# WikiVector

**Semantic Search for Wikipedia Articles using Vector Embeddings**  

WikiVector is a production-ready pipeline that ingests Wikipedia dumps, transforms text into embeddings, stores them in a vector database (FAISS), and exposes a FastAPI endpoint for semantic queries.  
This project demonstrates modern **Data Engineering**, **Cloud-Readiness**, and **AI/Vector Database** skills.

---

## **Features**
- ✅ Download and parse large Wikipedia XML dumps
- ✅ Clean and split articles into paragraphs
- ✅ Generate vector embeddings using **SentenceTransformers**
- ✅ Store embeddings in **FAISS** for fast semantic search
- ✅ Expose a **FastAPI** endpoint for queries
- ✅ Dockerized for production deployment
- 🚀 Optional: Schedule ETL with Airflow or Prefect
- 📦 Optional: Store raw + processed data in **S3 / PostgreSQL**
- 🔍 Showcase: Semantic search over millions of Wikipedia paragraphs

---

## **Architecture**

```text
       +----------------+
       | Wikipedia Dump |
       +--------+-------+
                |
                v
          +-----------+
          | ETL Layer |
          |  - Clean  |
          |  - Split  |
          +-----+-----+
                |
                v
      +--------------------+
      | Vector Embeddings  |
      |  - SentenceTransformer  |
      |  - FAISS Index     |
      +---------+----------+
                |
                v
          +-----------+
          | FastAPI   |
          |  Endpoint |
          +-----------+
                |
                v
          +-----------+
          | User / UI |
          +-----------+
