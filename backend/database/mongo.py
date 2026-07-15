import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI is missing! Please add it to your .env file.")

print("⏳ Connecting to MongoDB Atlas...")
try:
    # Connect to the cloud cluster
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Ping the server to verify connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"Failed to connect to MongoDB Atlas: {e}")

# Create/select the database and collections
db = client["techmart_ai"]
users_collection = db["users"]
chats_collection = db["chats"]