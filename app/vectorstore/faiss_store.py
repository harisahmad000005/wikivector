import faiss, numpy as np

index = faiss.IndexFlatL2(384)
documents = []

def upsert_text(text, vector):
    index.add(np.array([vector]).astype("float32"))
    documents.append(text)
