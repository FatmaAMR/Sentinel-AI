from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import login, verify_token
from models import Token
from database import USERS_DB, hash_password, blacklist_token

router = APIRouter()

# بيحدد فين الـ login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# دالة بتجيب الـ user الحالي من الـ Token
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token غلط أو منتهي",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# دالة بتتحقق من الـ role
def require_role(*roles):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="مش مسموحلك تدخل هنا"
            )
        return current_user
    return role_checker

# ==================== Login ====================
@router.post("/login", response_model=Token)
def login_route(form_data: OAuth2PasswordRequestForm = Depends()):
    token = login(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو الباسورد غلط"
        )
    return {"access_token": token, "token_type": "bearer"}
@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), user: dict = Depends(get_current_user)):
    blacklist_token(token)
    return {"message": f"تم تسجيل خروج {user['username']} بنجاح"}

# ==================== Operator Routes ====================
@router.get("/operator/alerts")
def review_alerts(user: dict = Depends(require_role("operator"))):
    return {"message": f"مرحباً {user['username']}!", "alerts": ["Alert 1", "Alert 2"]}

@router.get("/operator/plan")
def plan_maintenance(user: dict = Depends(require_role("operator"))):
    return {"message": "خطة الصيانة", "plan": "Maintenance scheduled"}

@router.post("/operator/feedback")
def provide_feedback(user: dict = Depends(require_role("operator"))):
    return {"message": "تم استلام الـ Feedback"}

@router.get("/operator/ai-clarification")
def ask_ai(user: dict = Depends(require_role("operator"))):
    return {"message": "AI Clarification هنا"}

# ==================== Technical Team Routes ====================
@router.get("/technical/alerts")
def escalated_alerts(user: dict = Depends(require_role("technical_team"))):
    return {"message": "Escalated Alerts", "alerts": ["Critical Alert 1"]}

@router.get("/technical/recommended-actions")
def recommended_actions(user: dict = Depends(require_role("technical_team"))):
    return {"message": "Recommended Actions", "actions": ["Action 1", "Action 2"]}

# ==================== Production Manager Routes ====================
@router.get("/manager/reports")
def summary_reports(user: dict = Depends(require_role("production_manager"))):
    return {"message": "Summary Reports", "data": "Report Data"}

@router.get("/manager/dashboard")
def dashboard(user: dict = Depends(require_role("production_manager"))):
    return {"message": "Dashboard Data", "graphs": "Real-time Graphs"}
from database import USERS_DB, hash_password
from models import LoginRequest

@router.post("/register")
def register(user_data: LoginRequest, role: str):
    # تتأكد إن الـ role صح
    valid_roles = ["operator", "technical_team", "production_manager"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"الـ role لازم يكون: {valid_roles}"
        )
    # تتأكد إن الـ username مش موجود
    if user_data.username in USERS_DB:
        raise HTTPException(
            status_code=400,
            detail="الـ username موجود بالفعل"
        )
    # إضافة الـ user الجديد
    USERS_DB[user_data.username] = {
        "username": user_data.username,
        "password": hash_password(user_data.password),
        "role": role
    }
    return {"message": f"تم تسجيل {user_data.username} بنجاح كـ {role}"}
# ==================== Admin Routes ====================
@router.get("/admin/users")
def get_all_users(user: dict = Depends(require_role("admin"))):
    users = []
    for username, data in USERS_DB.items():
        users.append({"username": username, "role": data["role"]})
    return {"users": users}

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