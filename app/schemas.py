from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    query: str
    ticket_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    confidence: float
    escalated: bool
    ticket_id: Optional[str] = None


class HitlResponseRequest(BaseModel):
    ticket_id: str
    response: str
