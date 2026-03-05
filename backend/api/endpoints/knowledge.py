from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.models import KnowledgeBase
from ..schemas.knowledge import KnowledgeResponse
import shutil
import os

router = APIRouter()
UPLOAD_DIR = "data/manuals"

@router.post("/upload")
async def upload_manual(file: UploadFile = File(...), db: Session = Depends(get_db)):
    existing_file = db.query(KnowledgeBase).filter(KnowledgeBase.file_name == file.filename).first()
    
    if existing_file:
        raise HTTPException(
            status_code=400, 
            detail=f"The Resource '{file.filename}'is alraedy exist! If You want to upload another version Drop The Old one!"
        )

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        new_file = KnowledgeBase(file_name=file.filename, file_path=file_path)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
        
        return {"status": "success", "id": new_file.id, "filename": file.filename}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/", response_model=List[KnowledgeResponse])
async def get_all_manuals(db: Session = Depends(get_db)):
    return db.query(KnowledgeBase).all()

@router.get("/{file_id}")
async def get_manual(file_id: int, db: Session = Depends(get_db)):
    manual = db.query(KnowledgeBase).filter(KnowledgeBase.id == file_id).first()
    if not manual:
        raise HTTPException(status_code=404, detail="Manual not found")
    return manual


@router.delete("/{file_id}")
async def delete_manual(file_id: int, db: Session = Depends(get_db)):
    manual = db.query(KnowledgeBase).filter(KnowledgeBase.id == file_id).first()
    if not manual:
        raise HTTPException(status_code=404, detail="Manual not found")
    
    try:
        if os.path.exists(manual.file_path):
            os.remove(manual.file_path)

        db.delete(manual)
        db.commit()
        return {"status": "deleted", "message": f"File {manual.file_name} removed"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")