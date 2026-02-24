from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.models import KnowledgeBase
import shutil
import os

router = APIRouter()
UPLOAD_DIR = "manuals"

@router.post("/upload")
async def upload_manual(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    new_file = KnowledgeBase(file_name=file.filename, file_path=file_path)
    db.add(new_file)
    db.commit()
    # هنا هنادي على ميثود الـ Ingestion للـ VDB لاحقاً
    return {"message": f"File {file.filename} uploaded and metadata saved."}

@router.get("/files")
def list_files(db: Session = Depends(get_db)):
    return db.query(KnowledgeBase).all()

@router.delete("/files/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(KnowledgeBase).filter(KnowledgeBase.id == file_id).first()
    if not file: raise HTTPException(status_code=404)
    if os.path.exists(file.file_path): os.remove(file.file_path)
    db.delete(file)
    db.commit()
    return {"message": "Deleted successfully"}