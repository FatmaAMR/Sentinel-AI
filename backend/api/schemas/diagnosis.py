from pydantic import BaseModel
from datetime import datetime

class DiagnosisRequest(BaseModel):
    logs: str

class DiagnosisResponse(BaseModel):
    reading_id: str
    severity: str  # NORMAL, WATCH, CRITICAL
    fault_type: str
    action_plan: str
    confidence_score: float
    timestamp: datetime
    
    class Config:
        from_attributes = True