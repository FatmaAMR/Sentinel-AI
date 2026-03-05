from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import DiagnosisRequest, DiagnosisResponse
from ..services import rag_engine
from ..core import get_db

router = APIRouter()

@router.post("/diagnose", response_model=DiagnosisResponse)
async def get_diagnosis(request: DiagnosisRequest, db: Session = Depends(get_db)):
    try:
        return rag_engine.get_diagnosis(request, db) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))