from app.services.wiki_client import fetch_wikipedia_chunks
from app.vectorstore.qdrant_store import upsert_text
from sentence_transformers import SentenceTransformer
from app.core.config import EMBEDDING_MODEL
from app.core.db import SessionLocal
from app.models import WikiArticle

model = SentenceTransformer(EMBEDDING_MODEL)
db = SessionLocal()

def ingest_article(title: str):
    # Check if already ingested
    article = db.query(WikiArticle).filter_by(page_title=title).first()
    if article and article.ingested:
        return f"Article '{title}' already ingested."

    # Fetch chunks from Wikipedia
    chunks = fetch_wikipedia_chunks(title)

    # Embed & store in Qdrant
    for idx, chunk in enumerate(chunks):
        vector = model.encode(chunk)
        upsert_text(chunk, vector, metadata={"page_title": title, "section_index": idx})

    # Store relational info in PostgreSQL
    if not article:
        article = WikiArticle(page_title=title, chunk_count=len(chunks), ingested=True)
        db.add(article)
    else:
        article.chunk_count = len(chunks)
        article.ingested = True

    db.commit()
    return f"Ingested {len(chunks)} chunks for '{title}'."
