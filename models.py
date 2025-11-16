from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: str
    explanation: str

class QuizSchema(BaseModel):
    title: str
    summary: str
    quiz: List[Question]
    related_topics: List[str]
