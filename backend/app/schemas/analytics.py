from pydantic import BaseModel
from typing import List, Any

class KPI(BaseModel):
    name: str
    value: Any

class KPIsResponse(BaseModel):
    kpis: List[KPI]
