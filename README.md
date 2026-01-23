# WikiVector

**WikiVector** is a FastAPI-based application that extracts Wikipedia content, transforms it into vector embeddings, and stores it in a **Qdrant vector database** for **semantic search**. It allows you to query Wikipedia topics semantically, returning the most relevant sections of articles.

---

## Features

*  Fetch and parse Wikipedia articles using the MediaWiki API
*  Clean and chunk text for embeddings (~500 words per chunk)
*  Generate embeddings with **SentenceTransformers**
*  Store vectors in **Qdrant** for fast semantic search
*  Background ingestion via FastAPI `/ingest` endpoint
*  Semantic search via `/search` endpoint
*  Dockerized for local development and production
*  Persistent vector storage using Docker volumes

---

## Architecture Overview

```text
Wikipedia API
     │
     ▼
ETL Pipeline (clean → chunk → embed)
     │
     ▼
Qdrant Vector DB
     │
     ▼
FastAPI API Endpoints
```

**Components**

| Component                         | Purpose                                   |
| --------------------------------- | ----------------------------------------- |
| `app/main.py`                     | FastAPI app entry point                   |
| `app/api/routes.py`               | API endpoints (`/ingest`, `/search`)      |
| `app/services/wiki_client.py`     | Fetch Wikipedia content                   |
| `app/etl/wiki_etl.py`             | Clean, chunk, embed, store in Qdrant      |
| `app/vectorstore/qdrant_store.py` | Qdrant client + search logic              |
| `app/core/config.py`              | Centralized environment/config management |

---

## Requirements

* Python 3.11+
* Docker & Docker Compose
* Internet connection (for Wikipedia API and embeddings)
* `.env` file in project root

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/wikivector.git
cd wikivector
```

2. Create a `.env` file in the root directory:

```env
APP_NAME=wikivector
ENV=local

QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=wikivector_embeddings

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_SIZE=384
```

3. Build and run the project using Docker Compose:

```bash
docker compose up --build
```

* FastAPI: `http://localhost:8000`
* Qdrant: `http://localhost:6333`

---

## API Endpoints

### Health Check

```http
GET /health
```

**Response**

```json
{
  "status": "ok"
}
```

---

### Ingest Wikipedia Topic

```http
POST /ingest?topic=Python_(programming_language)
```

**What it does:**

1. Fetches Wikipedia page via MediaWiki API
2. Cleans and chunks the text (~500 words per chunk)
3. Generates embeddings using SentenceTransformers
4. Stores embeddings in Qdrant along with metadata:

   * `page_title`
   * `section_index`
   * `text` chunk

**Response**

```json
{
  "message": "ETL started"
}
```

---

### Semantic Search

```http
POST /search
Content-Type: application/json

{
  "query": "How does Python handle object-oriented programming?",
  "top_k": 5
}
```

**Workflow:**

1. Embeds the query using the same model as ETL
2. Performs nearest-neighbor search in Qdrant
3. Returns top `k` relevant chunks with metadata

**Example Response**

```json
[
  {
    "text": "Python supports object-oriented programming with classes and inheritance...",
    "page_title": "Python (programming language)",
    "section_index": 2,
    "score": 0.94
  },
  {
    "text": "Classes in Python allow encapsulation of data and functions...",
    "page_title": "Python (programming language)",
    "section_index": 3,
    "score": 0.91
  }
]
```

---

## ETL & Vector Storage Details

* **ETL**:

  * Fetch Wikipedia content with `wikipedia` library / MediaWiki API
  * Clean sections (remove references, tables, markup)
  * Chunk text (~500 words per chunk)
  * Generate embeddings using **SentenceTransformers**

* **Qdrant**:

  * Stores vectors and metadata
  * Vector size: 384
  * Distance metric: Cosine
  * Collection auto-created if missing

* **Metadata stored**:

  * `page_title` → Wikipedia page title
  * `section_index` → chunk index in page
  * `text` → actual chunk

---

## Docker Notes

* Qdrant stores vectors in Docker volume for persistence
* FastAPI connects to Qdrant using `.env` configuration
* The app works **locally and in production** with the same configuration
* Recommended workflow:

  1. `docker compose up -d qdrant`
  2. `docker compose up --build api`

---

## Future Improvements

* Async ingestion using **Celery + Redis**
* Rate-limiting and retries for Wikipedia API
* Multi-language Wikipedia ingestion
* OpenAI embeddings for larger models
* Enhanced `/search` with filters and snippet highlighting

---

## References

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [Qdrant Documentation](https://qdrant.tech/documentation/)
* [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page)
* [SentenceTransformers](https://www.sbert.net/)

