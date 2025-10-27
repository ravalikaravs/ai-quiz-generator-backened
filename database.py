# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your MySQL credentials
DB_USER = "root"
DB_PASSWORD = "root123"
DB_HOST = "localhost"
DB_NAME = "quiz_db"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500))
    title = Column(String(200))
    date_generated = Column(DateTime)
    scraped_content = Column(Text)
    full_quiz_data = Column(Text)

# Create tables
Base.metadata.create_all(bind=engine)
