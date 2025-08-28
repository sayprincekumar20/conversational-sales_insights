from pydantic import BaseModel
from typing import Optional, List, Dict

class QueryRequest(BaseModel):
    prompt: str
    chart_type: Optional[str] = "auto"

class QueryResponse(BaseModel):
    sql: str
    data: List[Dict]
    chart: Dict
    summary: str
    forecast: Optional[Dict] = None   # ⬅️ new field
