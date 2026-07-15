# backend/agents/base_agent.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Load environment variables
load_dotenv()

# 2. Configure the Gemini API
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    print("⚠️ WARNING: GOOGLE_API_KEY not found in .env file!")
else:
    genai.configure(api_key=google_api_key)

class BaseSupportAgent:
    def __init__(self, agent_name: str, system_instructions: str):
        self.agent_name = agent_name
        self.system_instructions = system_instructions
        
        # Initialize the Gemini model (without the version-specific system_instruction flag)
        self.model = genai.GenerativeModel("gemini-3.1-flash-lite")

    def generate_response(self, user_message: str, context: str = "") -> str:
        """
        Takes the user's query (and optional RAG context), sends it to Gemini, 
        and returns the AI's answer.
        """
        try:
            # Combine everything into one master prompt with strict anti-hallucination rules
            prompt = f"System Instructions: {self.system_instructions}\n\n"
            
            if context:
                prompt += (
                    "STRICT KNOWLEDGE BASE CONTEXT:\n"
                    "You must base your answer ENTIRELY on the following text. "
                    "Do not invent facts, business hours, prices, or company policies. "
                    "If the answer cannot be found in this specific text, politely state that you do not have that information.\n"
                    f"{context}\n\n"
                )
            else:
                prompt += (
                    "No external context provided. Answer strictly based on your system instructions "
                    "and do not invent company policies or details.\n\n"
                )
                
            prompt += f"User Question: {user_message}"
                
            # Send to Google Gemini
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"❌ Gemini API Error: {e}")
            return "I apologize, but my connection is temporarily down. Please try again in a moment."