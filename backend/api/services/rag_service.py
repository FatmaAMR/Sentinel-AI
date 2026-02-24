import os
import json
import uuid
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from ..schemas.diagnosis import DiagnosisResponse 

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        self.vector_store = Chroma(
            persist_directory="./vectordb",
            embedding_function=self.embeddings
        )
        
        self.llm = ChatGroq(
            temperature=0, 
            model_name="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.template = """You are a Senior Maintenance Engineer. Analyze context to deliver a diagnostic report.
        
        CONTEXT: {context}
        LOG ENTRY: {input}
        
        STRICT REQUIREMENT: Output your response ONLY as a valid JSON object. 
        Do not include any introductory text. The JSON must have these keys:
        "severity": (Must be one of: NORMAL, WATCH, CRITICAL),
        "fault_type": (Brief name of the issue),
        "action_plan": (Concise steps for the team),
        "confidence_score": (A float between 0.0 and 1.0)
        """
        
        self.prompt = ChatPromptTemplate.from_template(self.template)

    def get_diagnosis(self, user_input: str) -> DiagnosisResponse:

        combine_docs_chain = create_stuff_documents_chain(self.llm, self.prompt)
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        chain = create_retrieval_chain(retriever, combine_docs_chain)
        
        
        result = chain.invoke({"input": user_input})
        
        try:
            data = json.loads(result["answer"])
            
            return DiagnosisResponse(
                reading_id=str(uuid.uuid4()),
                severity=data.get("severity", "WATCH"),
                fault_type=data.get("fault_type", "Unknown Issue"),
                action_plan=data.get("action_plan", "General inspection required"),
                confidence_score=float(data.get("confidence_score", 0.0)),
                timestamp=datetime.now()
            )
        except (json.JSONDecodeError, Exception) as e:
            return DiagnosisResponse(
                reading_id=str(uuid.uuid4()),
                severity="CRITICAL",
                fault_type="Analysis Error",
                action_plan=f"AI output parsing failed. Raw response: {result['answer'][:50]}...",
                confidence_score=0.0,
                timestamp=datetime.now()
            )

rag_engine = RAGService()