from pydantic import BaseModel
from typing import Optional

# بيانات اللي بيعمل Login
class LoginRequest(BaseModel):
    username: str
    password: str

# بيانات الـ Token اللي بترجع بعد Login
class Token(BaseModel):
    access_token: str
    token_type: str

# بيانات الـ User الجوه الـ Token
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# بيانات الـ User الكاملة
class User(BaseModel):
    username: str
    role: str  # operator, technical_team, production_manager