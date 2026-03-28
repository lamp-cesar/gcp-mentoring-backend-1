# AI Personal Trainer: Multi-Agent Workout Generator

A Python-based multi-agent system that generates hyper-personalized workout plans using AI. The system uses an autonomous refinement loop to ensure workout quality scores exceed 8.5/10 before delivery.

## Prerequisites

- Python 3.10 or later (3.12+ recommended)
- Poetry (dependency manager)
- Google API Key for Gemini access

## Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd gcp-mentoring-backend
```

### 2. Install Dependencies
```bash
make install
```

### 3. Configure Environment
Create a `.env` file in the project root with your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

### 4. Run the Application
```bash
make run
```

The FastAPI server starts on `http://localhost:8080`

## API Endpoint

**POST** `/generate-workout`

Request body:
```json
{
  "name": "John Doe",
  "age": 30,
  "weight": 75,
  "goal": "muscle_gain",
  "experience_level": "intermediate",
  "email": "john@example.com",
  "cellphone": "5511999999999"
}
```

Response: Personalized workout plan with exercise details, sets, reps, and rest periods.

## Available Commands

- `make install` — Install all dependencies using Poetry
- `make run` — Start the development server
- `make test` — Run tests with pytest
- `make lint` — Check code quality with ruff
- `make format` — Format code with black
- `make clean` — Remove build artifacts and cache

## Tech Stack

- **Framework**: FastAPI + Uvicorn
- **LLM**: Google Gemini 2.5 Flash
- **Dependency Management**: Poetry
- **Environment**: Python 3.10+

## Roadmap

- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions
- [ ] GCP Cloud Run deployment
- [ ] Advanced monitoring and logging
