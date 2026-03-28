# main.py (Raiz)
import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from models import Anamnesis
from agents.main import main as run_agents

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Health check status
_ready = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown events."""
    global _ready
    # Startup
    logger.info("Application startup initiated")
    _ready = True
    logger.info("Application is ready to receive requests")
    yield
    # Shutdown
    logger.info("Application shutdown initiated")
    _ready = False


app = FastAPI(
    title="AI Personal Trainer API",
    version="0.1.0",
    description="Multi-agent system for generating hyper-personalized workout plans",
    lifespan=lifespan
)


@app.get("/health", tags=["health"])
def health():
    """Liveness probe - always responds with 200 OK."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ai-personal-trainer"
    }


@app.get("/ready", tags=["health"])
def readiness():
    """Readiness probe - checks if application is ready to handle requests."""
    return {
        "status": "ready" if _ready else "not_ready",
        "ready": _ready,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/version", tags=["info"])
def version():
    """Return application version and metadata."""
    return {
        "version": "0.1.0",
        "service": "ai-personal-trainer",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/generate-workout", tags=["workout"])
def generate_workout(anamnesis: Anamnesis):
    """Generate a hyper-personalized workout plan based on user anamnesis."""
    logger.info(f"Generating workout for user: {anamnesis.name}")
    result = run_agents(anamnesis)
    logger.info(f"Workout generation completed for user: {anamnesis.name}")
    return result


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    workers = int(os.environ.get("WORKERS", 1))
    
    logger.info(f"Starting Uvicorn server on {host}:{port}")
    
    # Run with appropriate timeout for long-running requests
    uvicorn.run(
        app,
        host=host,
        port=port,
        workers=workers
    )