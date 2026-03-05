from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from api.services.auth_service import (
    login_user, register_user, verify_token, blacklist_token, USERS_DB
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ==================== Schemas ====================
class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

# ==================== Dependencies ====================
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token غلط أو منتهي"
        )
    return user

def require_role(*roles):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="مش مسموحلك تدخل هنا"
            )
        return current_user
    return role_checker

# ==================== Endpoints ====================
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = login_user(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو الباسورد غلط"
        )
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register(data: RegisterRequest):
    result = register_user(data.username, data.password, data.role)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), user: dict = Depends(get_current_user)):
    blacklist_token(token)
    return {"message": f"تم تسجيل خروج {user['username']} بنجاح"}

@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return user

# ==================== Admin ====================
@router.get("/admin/users")
def get_all_users(user: dict = Depends(require_role("admin"))):
    return {"users": [{"username": u, "role": d["role"]} for u, d in USERS_DB.items()]}

@router.delete("/admin/delete/{username}")
def delete_user(username: str, user: dict = Depends(require_role("admin"))):
    if username not in USERS_DB:
        raise HTTPException(status_code=404, detail="الـ user مش موجود")
    if username == "admin":
        raise HTTPException(status_code=400, detail="مينفعش تمسح الـ admin!")
    del USERS_DB[username]
    return {"message": f"تم مسح {username} بنجاح"}

@router.put("/admin/change-role/{username}")
def change_role(username: str, new_role: str, user: dict = Depends(require_role("admin"))):
    valid_roles = ["operator", "technical_team", "production_manager"]
    if new_role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"الـ role لازم يكون: {valid_roles}")
    if username not in USERS_DB:
        raise HTTPException(status_code=404, detail="الـ user مش موجود")
    USERS_DB[username]["role"] = new_role
    return {"message": f"تم تغيير role الـ {username} إلى {new_role}"}
from api.services.auth_service import generate_reset_token, reset_password

class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str

@router.post("/forgot-password")
def forgot_password(username: str):
    result = generate_reset_token(username)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.post("/reset-password")
def reset_pwd(data: ResetPasswordRequest):
    result = reset_password(data.reset_token, data.new_password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result