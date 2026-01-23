from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WikiArticle(Base):
    __tablename__ = "wiki_articles"
    id = Column(Integer, primary_key=True)
    page_title = Column(String, unique=True, index=True)
    ingested_at = Column(DateTime, default=datetime.utcnow)
    chunk_count = Column(Integer)
    ingested = Column(Boolean, default=False)

class UserQuery(Base):
    __tablename__ = "user_queries"
    id = Column(Integer, primary_key=True)
    query_text = Column(String, index=True)
    result_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
