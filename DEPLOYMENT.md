# Cloud Run Deployment Guide

This guide explains how to deploy the AI Personal Trainer API to Google Cloud Run.

## Prerequisites

- Google Cloud Project with billing enabled
- `gcloud` CLI installed and configured
- Docker installed (for local testing)
- Google Cloud Run API enabled

## Step 1: Set Up GCP Project

```bash
# Set your project ID
export PROJECT_ID=your-gcp-project-id
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com
```

## Step 2: Create Secret for API Key

Store your Google Gemini API key securely in Secret Manager:

```bash
# Create the secret
echo -n "your-gemini-api-key" | gcloud secrets create google-api-key --data-file=-

# Or update existing secret
echo -n "your-gemini-api-key" | gcloud secrets versions add google-api-key --data-file=-

# Grant Cloud Run service permission to access the secret
gcloud secrets add-iam-policy-binding google-api-key \
    --member=serviceAccount:PROJECT_ID@appspot.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor
```

Replace `PROJECT_ID` with your actual project ID.

## Step 3: Create Artifact Registry Repository

```bash
# Create Docker repository
gcloud artifacts repositories create gcp-mentoring-backend \
    --repository-format=docker \
    --location=us-central1 \
    --description="AI Personal Trainer API"

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev
```

Choose your preferred region (replace `us-central1` with `us-east1`, `us-west1`, `europe-west1`, etc.)

## Step 4: Build and Push Docker Image

```bash
# Set variables
export REGION=us-central1
export REPOSITORY=gcp-mentoring-backend
export SERVICE_NAME=ai-personal-trainer
export IMAGE_TAG=$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$SERVICE_NAME:latest

# Build Docker image
docker build -t $IMAGE_TAG .

# Push to Artifact Registry
docker push $IMAGE_TAG
```

Or use Cloud Build for automated builds:

```bash
gcloud builds submit \
    --tag=$IMAGE_TAG \
    --project=$PROJECT_ID
```

## Step 5: Deploy to Cloud Run

```bash
gcloud run deploy $SERVICE_NAME \
    --image=$IMAGE_TAG \
    --platform=managed \
    --region=$REGION \
    --memory=512Mi \
    --cpu=1 \
    --timeout=300 \
    --set-env-vars PORT=8080 \
    --set-secrets=GOOGLE_API_KEY=google-api-key:latest \
    --allow-unauthenticated \
    --health-check-disabled
```

### Deployment Parameters Explained

- `--memory=512Mi` — Allocated RAM (minimum recommended; adjust if needed)
- `--cpu=1` — CPU allocation
- `--timeout=300` — Request timeout (300 seconds for long multi-agent loops)
- `--set-secrets=GOOGLE_API_KEY=google-api-key:latest` — Inject secret as environment variable
- `--allow-unauthenticated` — Allow public access (remove if authorization required)
- `--health-check-disabled` — Cloud Run health checks are optional; remove if needed

## Step 6: Verify Deployment

```bash
# Get service URL
export SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')

echo "Service URL: $SERVICE_URL"

# Test health endpoint
curl $SERVICE_URL/health

# View API documentation
open $SERVICE_URL/docs

# Check logs
gcloud run logs read $SERVICE_NAME --region=$REGION --limit=50
```

## Step 7: Test the API

```bash
# Health check
curl -X GET $SERVICE_URL/health

# Readiness check
curl -X GET $SERVICE_URL/ready

# API docs
curl -X GET $SERVICE_URL/docs

# Generate workout (example request)
curl -X POST $SERVICE_URL/generate-workout \
    -H "Content-Type: application/json" \
    -d '{
        "name": "John Doe",
        "age": 30,
        "weight": 75,
        "goal": "muscle_gain",
        "experience_level": "intermediate",
        "email": "john@example.com",
        "cellphone": "5511999999999"
    }'
```

## Monitoring & Troubleshooting

### View Logs

```bash
# Real-time logs
gcloud run logs read $SERVICE_NAME --region=$REGION --follow

# Last 100 lines
gcloud run logs read $SERVICE_NAME --region=$REGION --limit=100
```

### Common Issues

#### 1. Secret Not Found

Error: `Error: Secret version not found`

**Solution:**
```bash
# Verify secret exists
gcloud secrets list

# Check service account has permission
gcloud secrets get-iam-policy google-api-key
```

#### 2. Request Timeout

Error: `504 Gateway Timeout` or request fails after 60 seconds

**Solution:** This is expected for multi-agent requests that take 30-120 seconds. Cloud Run default timeout is 60s; we set it to 300s in the deployment command. If still timing out:
- Increase `--timeout` value (max 3600s)
- Check Gemini API latency
- Review logs for specific bottlenecks

#### 3. Memory Exceeded

Error: `OOMKilled` or service continuously restarting

**Solution:**
```bash
# Increase memory allocation
gcloud run services update $SERVICE_NAME \
    --region=$REGION \
    --memory=1Gi
```

#### 4. Cold Starts Taking Too Long

This is normal (~5-10s on first request after deploy). Cloud Run will:
- Keep instances warm with traffic
- Create new instances if load increases

## Continuous Deployment (Optional)

### Using Cloud Build Triggers

Create automated deployments when code is pushed to a Git repository:

```bash
# Create a Cloud Build trigger
gcloud builds triggers create github \
    --name="ai-personal-trainer-deploy" \
    --repo-name="your-repo" \
    --repo-owner="your-username" \
    --branch-pattern="^main$" \
    --build-config="cloudbuild.yaml"
```

Create `cloudbuild.yaml` in project root:

```yaml
steps:
  # Build Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args: 
      - 'build'
      - '-t'
      - '$_REGION-docker.pkg.dev/$PROJECT_ID/$_REPOSITORY/$_SERVICE_NAME:latest'
      - '.'

  # Push to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - '$_REGION-docker.pkg.dev/$PROJECT_ID/$_REPOSITORY/$_SERVICE_NAME:latest'

  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - run
      - --image
      - '$_REGION-docker.pkg.dev/$PROJECT_ID/$_REPOSITORY/$_SERVICE_NAME:latest'
      - --location
      - $_REGION

substitutions:
  _REGION: 'us-central1'
  _REPOSITORY: 'gcp-mentoring-backend'
  _SERVICE_NAME: 'ai-personal-trainer'
```

## Configuration Reference

| Parameter | Default | Recommendation | Notes |
|-----------|---------|-----------------|-------|
| Memory | 256Mi | 512Mi | Peak usage ~300-500MB during processing |
| CPU | 0.083 (83m) | 1 | Mostly I/O-bound; 1 core sufficient |
| Timeout | 60s | 300s | Multi-agent loops take 30-120s |
| Concurrency | N/A | Default | Cloud Run manages instance scaling |
| Min Instances | 0 | 0 | Cost-effective; accept cold starts or set 1+ to minimize |

## Cost Estimation

Cloud Run pricing (as of March 2026):
- **Compute**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GB-second
- **Requests**: $0.40 per million requests
- **Small free tier**: 2 million requests/month

Example for 1000 requests/month with 5-minute processing time each:
- Compute: ~$0.08/month
- Memory: ~$0.01/month
- Total: ~$0.50/month (plus free tier allowance)

## Cleanup

```bash
# Delete the Cloud Run service
gcloud run services delete $SERVICE_NAME --region=$REGION

# Delete the Docker image
gcloud artifacts docker images delete \
    $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$SERVICE_NAME

# Delete the secret
gcloud secrets delete google-api-key
```
