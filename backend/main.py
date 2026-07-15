from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import bcrypt

# 1. Import your cloud database collections
from backend.database.mongo import users_collection, chats_collection

# 2. Import your local AI Engine
from backend.agents.base_agent import BaseSupportAgent

app = FastAPI()

# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize your primary AI agent when the server starts
print("⏳ Initializing TechMart AI Agent...")
support_agent = BaseSupportAgent(
    agent_name="TechMart Core Agent",
    system_instructions="You are a polite, helpful customer support agent for TechMart Electronics. Answer the user's questions clearly based on the provided company knowledge base."
)
print("✅ TechMart Agent ready for chat!")

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
        print("🧠 AI is processing through RAG and Gemini API...")
        
        ai_reply = support_agent.generate_response(request.message)
        
        chat_doc = {
            "session_id": request.session_id,
            "user_message": request.message,
            "bot_response": ai_reply
        }
        chats_collection.insert_one(chat_doc)
        
        print("✅ Response successfully generated and saved to DB.")
        
        return {"response": ai_reply}
        
    except Exception as e:
        print(f"❌ AI Generation Error: {e}")
        raise HTTPException(status_code=500, detail="The AI agents are currently offline or experiencing an error.")