from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json

VECTOR_FILE = "data/wiki_faiss.index"
MODEL_NAME = "all-MiniLM-L6-v2"
ARTICLES_FILE = "data/articles_cleaned.jsonl"

app = FastAPI()
model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(VECTOR_FILE)

# Load metadata
metadata = []
with open(ARTICLES_FILE) as f:
    for line in f:
        metadata.append(json.loads(line)["title"])

class Query(BaseModel):
    query: str
    top_k: int = 5

@app.post("/query")
def semantic_search(q: Query):
    q_vec = model.encode([q.query]).astype("float32")
    distances, indices = index.search(q_vec, q.top_k)
    results = [{"title": metadata[i], "score": float(distances[0][idx])} for idx, i in enumerate(indices[0])]
    return {"results": results}
