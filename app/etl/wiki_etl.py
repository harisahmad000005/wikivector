from sentence_transformers import SentenceTransformer
from app.services.wiki_client import fetch_page
from app.vectorstore.faiss_store import upsert_text

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk(text, size=500):
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i:i+size])

def run_wiki_etl(topic: str):
    text = fetch_page(topic)
    for c in chunk(text):
        vec = model.encode(c)
        upsert_text(c, vec)
