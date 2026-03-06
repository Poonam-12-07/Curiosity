from typing import List, Optional
from pydantic import BaseModel

class TaskBase(BaseModel):
    description: str
    is_completed: bool = False

class Task(TaskBase):
    id: int
    day_id: int
    class Config:
        from_attributes = True

class MathProblemBase(BaseModel):
    question: str
    answer: str

class MathProblem(MathProblemBase):
    id: int
    day_id: int
    class Config:
        from_attributes = True

class EnglishExerciseBase(BaseModel):
    sentence: str

class EnglishExercise(EnglishExerciseBase):
    id: int
    day_id: int
    class Config:
        from_attributes = True

class DayBase(BaseModel):
    name: str

class Day(DayBase):
    id: int
    tasks: List[Task] = []
    math_problems: List[MathProblem] = []
    english_exercises: List[EnglishExercise] = []
    class Config:
        orm_mode = True

class ChatMessage(BaseModel):
    message: str
