# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import json

from database import SessionLocal, Quiz  # Your SQLAlchemy setup
from scrapper import scrape_wikipedia      # Scraper function
from llm_quiz_generator import generate_quiz  # Your Gemini LLM generator

# Initialize FastAPI
app = FastAPI()

# CORS middleware to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def root():
    return {"message": "AI Quiz Generator backend running."}

# POST endpoint: Generate Quiz
@app.post("/generate_quiz")
def generate_quiz_api(request: dict, db: Session = Depends(get_db)):
    url = request.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    # Sc
