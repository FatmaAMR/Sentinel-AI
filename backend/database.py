# هنا بنخزن المستخدمين مؤقتاً (بدل Database حقيقية)
# الـ password بتتخزن مشفرة

from passlib.context import CryptContext

# اداة تشفير الـ password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# دالة تشفر الـ password
def hash_password(password: str):
    return pwd_context.hash(password)

# قاعدة بيانات وهمية فيها المستخدمين
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

# دالة بتجيب الـ user من الـ database
def get_user(username: str):
    if username in USERS_DB:
        return USERS_DB[username]
    return None

# دالة بتتحقق من الـ password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
# Blacklist للتوكنات اللي اتعمل لها logout
TOKEN_BLACKLIST = set()

def blacklist_token(token: str):
    TOKEN_BLACKLIST.add(token)

def is_token_blacklisted(token: str):
    return token in TOKEN_BLACKLIST