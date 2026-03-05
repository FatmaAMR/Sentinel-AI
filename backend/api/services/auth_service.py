from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# إعدادات الـ JWT
SECRET_KEY = "your_super_secret_key_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# تشفير الـ password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Blacklist للتوكنات
TOKEN_BLACKLIST = set()

# ==================== Password ====================
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# ==================== JWT ====================
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        if token in TOKEN_BLACKLIST:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if username is None:
            return None
        return {"username": username, "role": role}
    except JWTError:
        return None

def blacklist_token(token: str):
    TOKEN_BLACKLIST.add(token)

# ==================== Auth Logic ====================
# قاعدة بيانات مؤقتة
USERS_DB = {
    "admin": {
        "username": "admin",
        "password": hash_password("admin123"),
        "role": "admin"
    },
    "ahmed_operator": {
        "username": "ahmed_operator",
        "password": hash_password("operator123"),
        "role": "operator"
    },
    "sara_technical": {
        "username": "sara_technical",
        "password": hash_password("technical123"),
        "role": "technical_team"
    },
    "manager_ali": {
        "username": "manager_ali",
        "password": hash_password("manager123"),
        "role": "production_manager"
    }
}

def get_user(username: str):
    return USERS_DB.get(username)

def login_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user["password"]):
        return None
    return create_access_token({"sub": user["username"], "role": user["role"]})

def register_user(username: str, password: str, role: str):
    valid_roles = ["operator", "technical_team", "production_manager"]
    if role not in valid_roles:
        return {"error": f"الـ role لازم يكون: {valid_roles}"}
    if username in USERS_DB:
        return {"error": "الـ username موجود بالفعل"}
    USERS_DB[username] = {
        "username": username,
        "password": hash_password(password),
        "role": role
    }
    return {"success": f"تم تسجيل {username} بنجاح"}
# ==================== Forgot Password ====================
RESET_TOKENS = {}

def generate_reset_token(username: str):
    if username not in USERS_DB:
        return {"error": "الـ username مش موجود"}
    reset_token = jwt.encode(
        {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=15)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    RESET_TOKENS[username] = reset_token
    return {"reset_token": reset_token}

def reset_password(reset_token: str, new_password: str):
    try:
        payload = jwt.decode(reset_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in RESET_TOKENS:
            return {"error": "التوكن غلط أو منتهي"}
        if RESET_TOKENS[username] != reset_token:
            return {"error": "التوكن غلط"}
        USERS_DB[username]["password"] = hash_password(new_password)
        del RESET_TOKENS[username]
        return {"success": "تم تغيير الباسورد بنجاح"}
    except JWTError:
        return {"error": "التوكن منتهي أو غلط"}