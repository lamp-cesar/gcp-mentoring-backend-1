# agents/main.py
from .anamnesis_agent.main import anamnesis_main
from .personal_trainer_agent.main import workout_plan_main
from models import Anamnesis

def main(data: Anamnesis):
    anamnesis_result = anamnesis_main(data)
    workout_plan = workout_plan_main(anamnesis_result)
    return {"status": "success", "data": workout_plan}