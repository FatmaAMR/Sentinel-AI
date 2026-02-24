from fastapi import FastAPI
from api.core.database import engine, Base
from api.endpoints import chat, knowledge
from api.models import models
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sentinel AI")

app.include_router(chat.router, prefix="/chat")
app.include_router(knowledge.router, prefix="/knowledge")