from fastapi import APIRouter

router = APIRouter(prefix="/ingest")

@router.post("/run")
def run_ingest():
    return {"status": "scheduled"}
