from fastapi import APIRouter
from pydantic import BaseModel
from app.etl.wiki_etl import ingest_article
from app.vectorstore.qdrant_store import search_vector
from sentence_transformers import SentenceTransformer
from app.core.config import EMBEDDING_MODEL
from app.core.db import SessionLocal
from app.models import UserQuery

router = APIRouter()
model = SentenceTransformer(EMBEDDING_MODEL)
db = SessionLocal()

# ---- Ingest endpoint ----
@router.post("/ingest")
def ingest(topic: str):
    message = ingest_article(topic)
    return {"message": message}

# ---- Semantic search endpoint ----
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/search")
def semantic_search(request: SearchRequest):
    query_vec = model.encode(request.query)
    results = search_vector(query_vec, top_k=request.top_k)

    # Log user query
    db.add(UserQuery(query_text=request.query, result_count=len(results)))
    db.commit()

    return results

@router.get("/history")
def get_query_history(limit: int = 10):
    queries = db.query(UserQuery).order_by(UserQuery.created_at.desc()).limit(limit).all()
    return [
        {"query_text": q.query_text, "result_count": q.result_count, "created_at": q.created_at}
        for q in queries
    ]
