from pydantic import BaseModel
from datetime import datetime

class KnowledgeResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    upload_date: datetime

    class Config:
        from_attributes = True