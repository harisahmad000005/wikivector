import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

INPUT_FILE = "data/articles_cleaned.jsonl"
VECTOR_FILE = "data/wiki_faiss.index"
MODEL_NAME = "all-MiniLM-L6-v2"

os.makedirs("data", exist_ok=True)

def chunk_text(text, chunk_size=500):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i+chunk_size])

def build_faiss_index():
    model = SentenceTransformer(MODEL_NAME)
    texts = []
    metadata = []

    print("Generating embeddings...")
    with open(INPUT_FILE) as f:
        for line in f:
            article = json.loads(line)
            for chunk in chunk_text(article["text"]):
                texts.append(chunk)
                metadata.append(article["title"])
    
    embeddings = model.encode(texts, show_progress_bar=True)
    dim = embeddings.shape[1]
    
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    
    faiss.write_index(index, VECTOR_FILE)
    print(f"FAISS index saved to {VECTOR_FILE}")

if __name__ == "__main__":
    build_faiss_index()
