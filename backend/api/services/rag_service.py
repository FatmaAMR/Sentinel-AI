import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from ..core import settings
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# استيراد الإعدادات من الـ Core
from ..core import settings

# LangChain Imports (Remote-friendly)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ..schemas import DiagnosisResponse
from ..models.models import ChatHistory, DiagnosisLog

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        self.vector_store = Chroma(
            persist_directory="./data/vectordb",
            embedding_function=self.embeddings
        )
        

        self.llm = ChatGroq(
            temperature=0,
            model_name="llama-3.3-70b-versatile",
            api_key=settings.GROQ_API_KEY,
            groq_api_key=settings.GROQ_API_KEY
        )

        self.template = """
        You are a Senior Maintenance Engineer (Sentinel AI Expert).
        Use the following pieces of context and chat history to diagnose the machine fault.
        
        CONTEXT: {context}
        HISTORY: {history}
        LOGS: {input}
        
        Output ONLY a valid JSON object with these keys:
        {{
            "severity": "CRITICAL/WARNING/STABLE",
            "fault_type": "name of the fault",
            "action_plan": "step by step guide",
            "confidence_score": 0.0 to 1.0
        }}
        """
        self.prompt = ChatPromptTemplate.from_template(self.template)

    def get_diagnosis(self, request, db: Session) -> DiagnosisResponse:
        docs = self.vector_store.similarity_search(request.logs, k=3)
        context_text = "\n".join([d.page_content for d in docs])
        
        history_records = db.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).limit(3).all()
        history_text = "\n".join([f"User: {h.user_query}\nAI: {h.ai_response}" for h in history_records])

        chain = self.prompt | self.llm | StrOutputParser()
        raw_res = chain.invoke({
            "context": context_text,
            "history": history_text,
            "input": request.logs
        })

        try:
            data = json.loads(raw_res)
            
            # هـ- حفظ البيانات
            new_log = DiagnosisLog(
                machine_logs=request.logs,
                severity=data.get("severity", "STABLE"),
                fault_type=data.get("fault_type", "Unknown"),
                action_plan=data.get("action_plan", "Manual check required")
            )
            new_chat = ChatHistory(user_query=request.logs, ai_response=raw_res)
            
            db.add(new_log)
            db.add(new_chat)
            db.commit()

            return DiagnosisResponse(
                reading_id=str(uuid.uuid4()),
                severity=new_log.severity,
                fault_type=new_log.fault_type,
                action_plan=new_log.action_plan,
                confidence_score=data.get("confidence_score", 0.0),
                timestamp=datetime.utcnow()
            )
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to parse AI response: {str(e)}")


rag_engine = RAGService()