import os
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, Float, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Tables
class RawArticle(Base):
    __tablename__ = "articles_raw"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    xml = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class CleanedArticle(Base):
    __tablename__ = "articles_cleaned"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    paragraph = Column(Text)
    chunk_id = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
