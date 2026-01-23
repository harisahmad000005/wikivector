from fastapi import APIRouter
from pydantic import BaseModel
from app.vectorstore.qdrant_store import search_vector
from sentence_transformers import SentenceTransformer
from app.core.config import EMBEDDING_MODEL

router = APIRouter()
model = SentenceTransformer(EMBEDDING_MODEL)

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/search")
def semantic_search(request: SearchRequest):
    query_vec = model.encode(request.query)
    results = search_vector(query_vec, top_k=request.top_k)
    return results
