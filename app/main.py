from fastapi import FastAPI
from app.models import Base
from app.core.db import engine
from app.api.routes import router as api_router

# Create tables in PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WikiVector")

app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}
