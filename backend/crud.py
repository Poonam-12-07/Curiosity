from sqlalchemy.orm import Session
from . import models, schemas

def get_day(db: Session, day_id: int):
    return db.query(models.Day).filter(models.Day.id == day_id).first()

def get_day_by_name(db: Session, name: str):
    return db.query(models.Day).filter(models.Day.name == name).first()

def get_days(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Day).offset(skip).limit(limit).all()

def toggle_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.is_completed = not task.is_completed
        db.commit()
        db.refresh(task)
    return task
