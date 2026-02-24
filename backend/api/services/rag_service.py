from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from sqlalchemy.orm import Session
from ..models.models import ChatHistory, DiagnosisLog

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = Chroma(persist_directory="./vectordb", embedding_function=self.embeddings)
        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile")

    def diagnose_and_store(self, logs: str, db: Session):
        docs = self.vector_store.similarity_search(logs, k=2)
        context = "\n".join([d.page_content for d in docs])
        
        history = db.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).limit(3).all()
        history_text = "\n".join([f"User: {h.user_query}\nAI: {h.ai_response}" for h in history])

        prompt = f"Expert Knowledge: {context}\nChat History: {history_text}\nCurrent Logs: {logs}\nAnalyze and respond in JSON."
        
        response = self.llm.invoke(prompt)
        ai_content = response.content 

        new_diag = DiagnosisLog(machine_logs=logs, severity="WATCH", fault_type="Analysis", action_plan=ai_content)
        new_chat = ChatHistory(user_query=logs, ai_response=ai_content)
        
        db.add(new_diag)
        db.add(new_chat)
        db.commit()
        
        return ai_content

rag_engine = RAGService()