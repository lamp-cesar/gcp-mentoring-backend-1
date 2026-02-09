# main.py (Raiz)
from fastapi import FastAPI
from models import Anamnesis
from agents.main import main as run_agents

app = FastAPI(title="AI Personal Trainer API")

@app.post("/generate-workout")
def generate_workout(anamnesis: Anamnesis):
    result = run_agents(anamnesis)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)