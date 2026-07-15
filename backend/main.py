import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import bcrypt

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Import your cloud database collections
from backend.database.mongo import users_collection, chats_collection

# 2. Import your Multi-Agent Orchestrator (Replacing the BaseSupportAgent)
from backend.agents.orchestrator import MultiAgentOrchestrator

app = FastAPI()

# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Setup paths and load the Vector Database ---
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORSTORE_DIR = os.path.join(BACKEND_DIR, "vectorstore", "faiss_index")

print("🧠 Loading Google Gemini Embedding Model...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Safely load the database if it exists on startup
if os.path.exists(VECTORSTORE_DIR):
    print("💾 FAISS Vector Database found! Loading index...")
    db = FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    print("✅ FAISS Retriever successfully mounted.")
else:
    print("⚠️ WARNING: Vector index folder not found at startup! Running without RAG context.")
    retriever = None

# 3. Initialize your Multi-Agent Orchestrator when the server starts
print("⏳ Initializing TechMart Multi-Agent Orchestrator...")
orchestrator = MultiAgentOrchestrator()
print("✅ Multi-Agent System ready!")

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.get("/")
async def root():
    return {"message": "TechMart AI Backend is Live!"}

@app.post("/api/register")
def register_user(request: RegisterRequest):
    if users_collection.find_one({"email": request.email}):
        raise HTTPException(status_code=400, detail="Email is already registered.")
    
    hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
    
    user_doc = {
        "name": request.name,
        "email": request.email,
        "password": hashed_password.decode('utf-8')
    }
    users_collection.insert_one(user_doc)
    
    return {"message": "User registered successfully!"}

@app.post("/api/login")
def login_user(request: LoginRequest):
    user = users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password.")
        
    if not bcrypt.checkpw(request.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid email or password.")
        
    return {
        "message": "Login successful", 
        "user": {"name": user["name"], "email": user["email"]}
    }


@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    try:
        print(f"\n💬 Received message: {request.message}")
        print("🧠 AI is processing through RAG and Multi-Agent Orchestrator...")
        
        # Retrieve context text matching the user's message
        context = ""
        if retriever:
            print("🔍 Searching FAISS vector database for relevant documentation...")
            docs = retriever.invoke(request.message)
            # Combine the page_content fields of the top 3 chunks into a clean context block
            context = "\n".join([doc.page_content for doc in docs])
            if context:
                print("📝 Matching context found and injected into prompt.")
            else:
                print("❓ No highly relevant matches found in vector store. Passing query standard.")
        
        # --- NEW: Pass message AND context to the Orchestrator ---
        orchestrator_output = orchestrator.process_customer_query(
            query=request.message, 
            context=context
        )
        
        # Extract the final text from the orchestrator's dictionary output
        ai_reply = orchestrator_output["response"]
        
        # Save to database (Bonus: We are now tracking which agents were used in MongoDB!)
        chat_doc = {
            "session_id": request.session_id,
            "user_message": request.message,
            "bot_response": ai_reply,
            "routed_agents": orchestrator_output.get("routed_agents", [])
        }
        chats_collection.insert_one(chat_doc)
        
        print("✅ Response successfully generated and saved to DB.")
        
        return {"response": ai_reply}
        
    except Exception as e:
        print(f"❌ AI Generation Error: {e}")
        raise HTTPException(status_code=500, detail="The AI agents are currently offline or experiencing an error.")