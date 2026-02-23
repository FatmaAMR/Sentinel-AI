from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Sentinel AI API", version="1.0.0")

# Simple Schema for a Log Entry
class MaintenanceLog(BaseModel):
    asset_id: str
    vibration_level: float
    note: str

@app.get("/")
def read_root():
    return {"status": "Sentinel Online", "timestamp": datetime.now()}

@app.post("/diagnose")
async def initial_test(log: MaintenanceLog):
    # This is where the RAG + LLM logic will go later
    return {
        "asset_id": log.asset_id,
        "received_vibration": log.vibration_level,
        "initial_diagnosis": "System receiving data. AI Engine Pending Integration.",
        "status": "Success"
    }