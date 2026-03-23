from pydantic import BaseModel

class Anamnesis(BaseModel):
    name: str
    age: int
    weight: float
    goal: str
    experience_level: str
    email: str
    cellphone: str
    
class WorkoutReview(BaseModel):
    score: float
    adjustments: str
    is_safe: bool

class FinalWorkoutResponse(BaseModel):
    anamnesis_summary: str
    workout_plan: str
    review: WorkoutReview
    attempts: int