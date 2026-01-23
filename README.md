# WikiVector

**WikiVector** is a **FastAPI-based application** that fetches Wikipedia content, transforms it into vector embeddings, stores them in **Qdrant** for semantic search, and uses **PostgreSQL via SQLAlchemy** to track relational info, logs, and user queries.

This architecture allows you to:

* Search Wikipedia **by meaning**, not just keywords
* Track ingested articles to **avoid duplicates**
* Log user queries for analytics and dashboards

---

## Features

* ✅ Fetch and parse Wikipedia articles
* ✅ Chunk text (~500 words per chunk)
* ✅ Generate embeddings with **SentenceTransformers**
* ✅ Store vectors + payload in **Qdrant** for fast semantic search
* ✅ Store relational metadata in **PostgreSQL** (SQLAlchemy)
* ✅ ETL + ingestion logs for production-grade workflow
* ✅ API endpoints for `/ingest`, `/search`, `/history`
* ✅ Dockerized for easy local and production deployment

---

## Architecture Overview

```text
                ┌─────────────┐
                │ Wikipedia   │
                │ API         │
                └─────┬───────┘
                      │
                      ▼
                 ETL Pipeline
          (clean → chunk → embed)
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   Qdrant Vector DB          PostgreSQL (SQLAlchemy)
   (vectors + payload)       (articles, logs, queries)
          │                       │
          └───────────┬───────────┘
                      ▼
                FastAPI Endpoints
      (/ingest, /search, /history)
```

---

## Requirements

* Python 3.11+
* Docker & Docker Compose
* Internet connection (Wikipedia API & embeddings)
* `.env` file in project root

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/wikivector.git
cd wikivector
```

2. Create a `.env` file:

```env
# App
APP_NAME=wikivector
ENV=local

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=wikivector_embeddings

# PostgreSQL
POSTGRES_URL=postgresql://wikivector:password@postgres:5432/wikivector_db

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_SIZE=384
```

3. Start Docker services:

```bash
docker compose up --build
```

* FastAPI: `http://localhost:8000`
* Qdrant: `http://localhost:6333`
* PostgreSQL: `localhost:5432`

---

## API Endpoints

### Health Check

```http
GET /health
```

**Response:**

```json
{"status": "ok"}
```

---

### 1️⃣ Ingest Wikipedia Article

```http
POST /ingest?topic=Python_(programming_language)
```

**Workflow:**

1. Checks PostgreSQL to avoid duplicates
2. Fetches Wikipedia content → chunks → embeddings
3. Stores vectors + metadata in Qdrant
4. Stores ingestion info in PostgreSQL

**Response:**

```json
{"message": "Ingested 10 chunks for 'Python_(programming_language)'"}
```

---

### 2️⃣ Semantic Search

```http
POST /search
Content-Type: application/json

{
  "query": "object-oriented programming in Python",
  "top_k": 5
}
```

**Workflow:**

1. Convert query → embedding
2. Qdrant searches nearest vectors → returns payload
3. Logs query in PostgreSQL

**Example Response:**

```json
[
  {
    "text": "Python supports object-oriented programming with classes and inheritance...",
    "page_title": "Python (programming language)",
    "section_index": 2,
    "score": 0.94
  }
]
```

---

### 3️⃣ Query History

```http
GET /history?limit=10
```

**Response:**

```json
[
  {"query_text": "object-oriented programming in Python", "result_count": 5, "created_at": "2026-01-23T10:15:00"},
  ...
]
```

* Allows analytics, dashboards, and auditing user queries

---

## ETL & Storage

### Qdrant

* Stores vectors and payload (text + metadata)
* Vector size: 384
* Distance metric: Cosine
* Supports **payload filtering** (like SQL “WHERE”)

### PostgreSQL

* Stores relational data: ingested articles, logs, query history
* Enables filtering, joins, and analytics
* Prevents re-ingesting same pages

---

## Docker Compose Overview

```yaml
services:
  api: FastAPI app
  qdrant: Vector DB
  postgres: Relational DB
```

* Persistent volumes for Qdrant & PostgreSQL
* Environment variables stored in `.env`

---

## Example Workflow

1. **Ingest article:** `/ingest?topic=Python_(programming_language)`
2. **Search semantically:** `/search` with your query
3. **Check query history:** `/history`

This ensures **semantic search + relational tracking** work seamlessly.

---

## Future Improvements

* Async ingestion via Celery + Redis
* Rate-limiting & retries for Wikipedia API
* Multi-language Wikipedia ingestion
* OpenAI embeddings for better accuracy
* Advanced filtering & analytics dashboards

---

## References

* [FastAPI](https://fastapi.tiangolo.com/)
* [Qdrant](https://qdrant.tech/documentation/)
* [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page)
* [SentenceTransformers](https://www.sbert.net/)
* [SQLAlchemy](https://www.sqlalchemy.org/)

---