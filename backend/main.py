from fastapi import FastAPI
from routes import router

# إنشاء الـ app
app = FastAPI(
    title="Predictive Maintenance Auth System",
    description="JWT Authentication & Authorization",
    version="1.0.0"
)

# تسجيل الـ routes
app.include_router(router)

# للتأكد إن الـ app شغال
@app.get("/")
def root():
    return {"message": "الـ API شغالة! روح على /docs"}