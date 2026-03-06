from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Check if data exists
    if db.query(models.Day).first():
        print("Data already exists.")
        return

    days_data = [
        {
            "name": "Sunday", 
            "task": ["THE", "OF", "AND"], 
            "math": ["2 + 3 = 5", "1 + 1 = 2", "2 x 2 = 4"], 
            "english": "I see the cat."
        },
        {
            "name": "Monday", 
            "task": ["A", "TO", "IN"], 
            "math": ["1 + 4 = 5", "2 + 2 = 4", "3 + 0 = 3"], 
            "english": "The dog is big."
        },
        {
            "name": "Tuesday", 
            "task": ["IS", "YOU", "THAT"], 
            "math": ["5 + 1 = 6", "3 + 3 = 6", "10 - 2 = 8"], 
            "english": "I like to play."
        },
        {
            "name": "Wednesday", 
            "task": ["IT", "HE", "WAS"], 
            "math": ["7 + 2 = 9", "4 + 4 = 8", "5 - 1 = 4"], 
            "english": "She has a ball."
        },
        {
            "name": "Thursday", 
            "task": ["FOR", "ON", "ARE"], 
            "math": ["6 + 4 = 10", "5 + 5 = 10", "2 x 3 = 6"], 
            "english": "The sun is hot."
        },
        {
            "name": "Friday", 
            "task": ["AS", "WITH", "HIS"], 
            "math": ["8 + 0 = 8", "1 + 5 = 6", "2 x 4 = 8"], 
            "english": "We go to school."
        },
        {
            "name": "Saturday", 
            "task": ["THEY", "I", "AT"], 
            "math": ["9 + 1 = 10", "3 + 2 = 5", "6 - 3 = 3"], 
            "english": "My mom is nice."
        }
    ]

    for data in days_data:
        day = models.Day(name=data["name"])
        db.add(day)
        db.commit()
        db.refresh(day)
        
        for word in data["task"]:
            # Storing Sight Words in the 'Task' model
            task = models.Task(description=word, day_id=day.id)
            db.add(task)

        # Add 2 Math problems
        for math_str in data["math"]:
            # naive parse "Q = A"
            parts = math_str.split('=')
            q = parts[0].strip()
            a = parts[1].strip()
            math = models.MathProblem(question=q, answer=a, day_id=day.id)
            db.add(math)
        
        english = models.EnglishExercise(sentence=data["english"], day_id=day.id)
        db.add(english)
    
    db.commit()
    print("Database seeded successfully.")
    db.close()

if __name__ == "__main__":
    seed_data()
