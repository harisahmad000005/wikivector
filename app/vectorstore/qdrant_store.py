from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, ScoredPoint
import numpy as np
from app.core.config import QDRANT_URL, QDRANT_COLLECTION, VECTOR_SIZE

client = QdrantClient(url=QDRANT_URL)

# Create collection if it doesn't exist
if QDRANT_COLLECTION not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance="Cosine")
    )

def upsert_text(text: str, vector: np.ndarray, metadata: dict = None):
    if metadata is None:
        metadata = {}
    client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=[
            {
                "id": None,
                "vector": vector.tolist(),
                "payload": {"text": text, **metadata}
            }
        ]
    )

def search_vector(query_vector: np.ndarray, top_k: int = 5):
    response = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_vector.tolist(),
        limit=top_k
    )
    results = [
        {
            "text": hit.payload["text"],
            "page_title": hit.payload.get("page_title"),
            "section_index": hit.payload.get("section_index"),
            "score": hit.score
        }
        for hit in response
    ]
    return results
