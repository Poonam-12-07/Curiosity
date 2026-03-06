from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Day(Base):
    __tablename__ = "days"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    tasks = relationship("Task", back_populates="day")
    math_problems = relationship("MathProblem", back_populates="day")
    english_exercises = relationship("EnglishExercise", back_populates="day")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean, default=False)
    day_id = Column(Integer, ForeignKey("days.id"))
    
    day = relationship("Day", back_populates="tasks")

class MathProblem(Base):
    __tablename__ = "math_problems"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)
    day_id = Column(Integer, ForeignKey("days.id"))
    
    day = relationship("Day", back_populates="math_problems")

class EnglishExercise(Base):
    __tablename__ = "english_exercises"
    id = Column(Integer, primary_key=True, index=True)
    sentence = Column(String)
    day_id = Column(Integer, ForeignKey("days.id"))
    
    day = relationship("Day", back_populates="english_exercises")
