from fastapi import FastAPI
from api.core.database import engine, Base
# هنا المشكلة: لازم تتأكد إن operations مكتوبة في السطر ده
from api.endpoints import chat, knowledge, auth, operations 
from api.models import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sentinel AI")

app.include_router(chat.router, prefix="/chat")
app.include_router(knowledge.router, prefix="/knowledge")
app.include_router(auth.router)
app.include_router(operations.router)