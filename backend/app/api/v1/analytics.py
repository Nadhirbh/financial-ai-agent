from fastapi import APIRouter

router = APIRouter(prefix="/analytics")

@router.get("/kpis")
def kpis():
    return {"kpis": []}
