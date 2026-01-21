from fastapi import APIRouter, BackgroundTasks
from app.etl.wiki_etl import run_wiki_etl

router = APIRouter()

@router.post("/ingest")
def ingest(topic: str, bg: BackgroundTasks):
    bg.add_task(run_wiki_etl, topic)
    return {"message": "ETL started"}
