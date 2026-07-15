import os
import pickle
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

def train_escalation_detector():
    print("⏳ Downloading the CFPB dataset from Hugging Face...")
    dataset = load_dataset("claritystorm/cfpb-consumer-complaints", split="train")
    
    # We now know EXACTLY what the column is called from your terminal output!
    text_column = "consumer_narrative"

    print(f"📊 Extracting text data directly from column: '{text_column}'")

    texts = []
    labels = []

    print("⚙️ Analyzing complaint narratives...")
    for row in dataset:
        narrative = row[text_column]
        
        # Skip empty rows or garbage data
        if not narrative or not isinstance(narrative, str) or len(narrative) < 10:
            continue
            
        texts.append(narrative)
        
        # Flag high-risk keywords as an Escalation to Human
        red_flags = ["sue", "lawyer", "attorney", "unacceptable", "illegal", "fraud", "court", "ignore", "scam"]
        if any(flag in narrative.lower() for flag in red_flags):
            labels.append("escalate_to_human")
        else:
            labels.append("handle_via_ai")
            
        # Cap at 5000 rows so your laptop trains it in seconds, not hours
        if len(texts) >= 5000:
            break

    print(f"🧠 Training Random Forest Escalation Classifier on {len(texts)} complaints...")
    model = make_pipeline(
        TfidfVectorizer(stop_words="english", max_features=3000),
        RandomForestClassifier(n_estimators=100, random_state=42)
    )
    
    model.fit(texts, labels)
    
    os.makedirs("backend/ml/artifacts", exist_ok=True)
    with open("backend/ml/artifacts/complaint_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("💾 Complete! Complaint Escalation Model saved safely to artifacts/complaint_model.pkl")

if __name__ == "__main__":
    train_escalation_detector()