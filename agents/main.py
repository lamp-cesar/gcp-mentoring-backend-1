# agents/main.py
from .anamnesis_agent.main import anamnesis_main
from .personal_trainer_agent.main import workout_plan_main
from .workout_validator_agent.main import workout_validator
from models import Anamnesis

def main(data: Anamnesis):
    anamnesis_result = anamnesis_main(data)
    
    attempt = 0
    max_attempts = 3
    current_score = 0.0
    workout_plan = ""
    last_review = {}

    while current_score < 8.5 and attempt < max_attempts:
        attempt += 1
        
        feedback = last_review.get("adjustments", "") if attempt > 1 else "First Version."
        
        workout_plan = workout_plan_main(anamnesis_result, feedback=feedback)
        
        validation_result = workout_validator(anamnesis_result, workout_plan)
        current_score = validation_result.get("score", 0.0)
        last_review = validation_result

        print(f"Tentativa {attempt}: Nota {current_score}")
        
    return {
        "status": "success",
        "attempts": attempt,
        "final_score": current_score,
        "data": {
            "anamnesis": anamnesis_result,
            "workout": workout_plan,
            "review": last_review
        }
    }