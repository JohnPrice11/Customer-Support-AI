import os
from dotenv import load_dotenv  # Ensure this is added to load your .env key
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # NEW
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

# 1. Get the directory where ingest.py lives (backend/rag/)
RAG_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to get the backend folder (backend/)
BACKEND_DIR = os.path.dirname(RAG_DIR)

# 3. Go up one more level to get the absolute root folder (customer-support-ai/)
BASE_DIR = os.path.dirname(BACKEND_DIR)

# 4. Correctly map the final directories
KB_DIR = os.path.join(BASE_DIR, "knowledge_base")
VECTORSTORE_DIR = os.path.join(BACKEND_DIR, "vectorstore", "faiss_index")

def build_vector_store():
    print(f"📂 Searching for PDFs in: {KB_DIR}")
    
    # 1. Load all PDFs from the knowledge_base folder
    loader = PyPDFDirectoryLoader(KB_DIR)
    documents = loader.load()
    
    if not documents:
        print("❌ Error: No PDFs found. Please check your knowledge_base directory.")
        return
        
    print(f"✅ Successfully loaded {len(documents)} pages from PDFs.")

    # 2. Chunk the text
    # A chunk size of 500-1000 with a small overlap ensures the LLM gets enough context 
    # without cutting off sentences in the middle of a policy.
    print("✂️ Splitting documents into semantic chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Generated {len(chunks)} text chunks.")

    # 3. Generate Embeddings 
    print("🧠 Initializing Google Gemini Embedding Model...")
    # Add the "gemini-" prefix to the model name
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # 4. Build and Save the FAISS Vector Database
    print("💾 Building FAISS vector index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Ensure the target directory exists
    os.makedirs(os.path.dirname(VECTORSTORE_DIR), exist_ok=True)
    
    vectorstore.save_local(VECTORSTORE_DIR)
    print(f"🎉 Success! Vector database saved locally at: {VECTORSTORE_DIR}")

if __name__ == "__main__":
    build_vector_store()