from jose import JWTError, jwt
from datetime import datetime, timedelta
from database import get_user, verify_password, is_token_blacklisted

# مفتاح سري لتشفير الـ Token (سري جداً!)
SECRET_KEY = "your_super_secret_key_123"
ALGORITHM = "HS256"
# الـ Token بيبقى صالح 30 دقيقة
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# دالة بتعمل Token جديد
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# دالة بتتحقق من الـ Token وبترجع بيانات الـ User
def verify_token(token: str):
    try:
        # بتتحقق لو التوكن في الـ Blacklist
        if is_token_blacklisted(token):
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if username is None:
            return None
        return {"username": username, "role": role}
    except JWTError:
        return None

# دالة بتتحقق من username و password وبترجع Token
def login(username: str, password: str):
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    # عمل Token فيه اسم الـ user والـ role بتاعه
    token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })
    return token