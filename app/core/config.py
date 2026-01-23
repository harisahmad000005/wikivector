from dotenv import load_dotenv
import os
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent  
load_dotenv(dotenv_path=BASE_DIR / ".env")

APP_NAME = os.getenv("APP_NAME", "wikivector")
ENV = os.getenv("ENV", "local")

# Qdrant config
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = os.getenv("QDRANT_PORT", "6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "wikivector_embeddings")
QDRANT_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"

# Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE", 384))
