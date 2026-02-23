"""
schemas in general for Data Validation.


Here for instanse Defines how Asset data should look when coming in (Request) or going out (Response)

"""
from pydantic import BaseModel
from typing import Optional

class AssetBase(BaseModel):
    name: str
    type: str
    location: str

class AssetCreate(AssetBase):
    pass # Data needed to create an asset

class Asset(AssetBase):
    id: str
    class Config:
        from_attributes = True # Allows compatibility with SQLAlchemy models