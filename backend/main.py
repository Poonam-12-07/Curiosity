from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from . import weather_report
from . import weather_agent
from .data import DAYS_DATA

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

@app.get("/days")
def read_days():
    return DAYS_DATA

@app.get("/days/{day_name}")
def read_day(day_name: str):
    day = next((d for d in DAYS_DATA if d["name"].lower() == day_name.lower()), None)
    if day is None:
        raise HTTPException(status_code=404, detail="Day not found")
    return day

@app.get("/weather")
def read_weather():
    try:
        weather_info = weather_report.get_weather(weather_report.CITY)
        return weather_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_with_agent(chat_msg: ChatMessage):
    try:
        reply = weather_agent.chat(chat_msg.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount the frontend directory
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
