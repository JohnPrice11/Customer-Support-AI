# backend/rag/retrieval.py
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTORSTORE_DIR = os.path.join(os.path.dirname(__file__), "../vectorstore/faiss_index")

class KnowledgeRetriever:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'}
        )
        self.db = None
        self._load_db()

    def _load_db(self):
        if os.path.exists(VECTORSTORE_DIR):
            self.db = FAISS.load_local(
                VECTORSTORE_DIR, 
                self.embeddings, 
                allow_dangerous_deserialization=True # Required for loading local FAISS pickling safely
            )
        else:
            self.db = None

    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """Searches the vector store and returns compiled text chunks."""
        if not self.db:
            return "No company documentation context available at this time."
        
        docs = self.db.similarity_search(query, k=top_k)
        context = "\n\n".join([f"[Source: {doc.metadata.get('source', 'Unknown')}]: {doc.page_content}" for doc in docs])
        return context