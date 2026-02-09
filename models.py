from pydantic import BaseModel

class Anamnesis(BaseModel):
    name: str
    age: int
    weight: float
    goal: str
    experience_level: str
    email: str
    cellphone: str