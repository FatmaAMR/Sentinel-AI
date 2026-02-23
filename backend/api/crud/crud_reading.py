"""
CRUD: Reading Operations.
Role: Handles Saving and Fetching vibration logs from SQLite.
Team Note: Use 'get_multi' to fetch data for the React charts.
"""
from sqlalchemy.orm import Session
from app.models import Reading

def create_reading(db: Session, vibration: float, asset_id: str):
    db_reading = Reading(vibration_value=vibration, asset_id=asset_id)
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

def get_asset_history(db: Session, asset_id: str, limit: int = 20):
    return db.query(Reading).filter(Reading.asset_id == asset_id).order_by(Reading.timestamp.desc()).limit(limit).all()