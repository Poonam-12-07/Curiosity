from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import SessionLocal, engine
from . import weather_report
from . import weather_agent

# Create database tables if they don't exist
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Note: Could not run create_all (expected on Vercel): {e}")

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/days", response_model=List[schemas.Day])
def read_days(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    days = crud.get_days(db, skip=skip, limit=limit)
    return days

@app.get("/days/{day_name}", response_model=schemas.Day)
def read_day(day_name: str, db: Session = Depends(get_db)):
    day = crud.get_day_by_name(db, name=day_name)
    if day is None:
        raise HTTPException(status_code=404, detail="Day not found")
    return day

@app.post("/tasks/{task_id}/toggle", response_model=schemas.Task)
def toggle_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.toggle_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/weather")
def read_weather():
    try:
        # Use the city from the weather_report config
        weather_info = weather_report.get_weather(weather_report.CITY)
        return weather_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_with_agent(chat_msg: schemas.ChatMessage):
    try:
        reply = weather_agent.chat(chat_msg.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.staticfiles import StaticFiles
import os

# Mount the frontend directory
# We go up one level from 'backend' to reach 'frontend'
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

