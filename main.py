# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import json
import re
from database import SessionLocal, Quiz
from scrapper import scrape_wikipedia
from llm_quiz_generator import generate_quiz

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "AI Quiz Generator backend running."}

@app.post("/generate_quiz")
def generate_quiz_api(request: dict, db: Session = Depends(get_db)):
    url = request.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        # Scrape Wikipedia
        title, scraped_text = scrape_wikipedia(url)

        if not scraped_text:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Failed to scrape content"}
            )
        quiz_data = generate_quiz(scraped_text)


        # Save to DB
        new_quiz = Quiz(
            url=url,
            title=title,
            scraped_content = scraped_text,
            full_quiz_data = json.dumps(quiz_data),
            date_generated=datetime.now()
        )
        db.add(new_quiz)
        db.commit()

        return {
            "status": "success",
            "quiz_id": new_quiz.id,
            "quiz": quiz_data
        }

    except Exception as e:
        print("Error:", e)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    try:
        quizzes = db.query(Quiz).order_by(Quiz.date_generated.desc()).all()
        result = [
            {
                "id": q.id,
                "title": q.title,
                "url": q.url,
                "date_generated": q.date_generated
            }
            for q in quizzes
        ]
        return {"status": "success", "history": result}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/quiz/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    try:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        return {
            "status": "success",
            "quiz": json.loads(quiz.full_quiz_data)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
