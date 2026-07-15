import os
import pickle
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

def train_intent_router():
    print("⏳ Downloading the official Banking77 dataset via Hugging Face...")
    # Programmatically fetches the dataset without needing manual CSV downloads
    dataset = load_dataset("banking77")
    train_data = dataset["train"]

    # Map the 77 banking categories into our 5 Custom Support Agents
    def map_to_agent(label_id):
        label_name = train_data.features["label"].names[label_id]
        
        # Categorize based on keywords in the original label
        if any(word in label_name for word in ["card", "payment", "charge", "refund", "fee"]):
            return "billing"
        elif any(word in label_name for word in ["pin", "password", "app", "activate", "error"]):
            return "technical"
        elif any(word in label_name for word in ["exchange", "limit", "verify", "rate"]):
            return "product"
        elif any(word in label_name for word in ["cancel", "compromise", "stolen", "terminate", "wrong"]):
            return "complaint"
        else:
            return "faq"

    print("⚙️ Processing and mapping 10,000+ rows of data...")
    texts = train_data["text"]
    labels = [map_to_agent(label_id) for label_id in train_data["label"]]

    print("🧠 Training the Machine Learning Router Pipeline...")
    # Create a pipeline that converts text to numbers (TF-IDF) and trains a classifier
    model = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_features=5000),
        LogisticRegression(solver='lbfgs', max_iter=1000)
    )
    
    model.fit(texts, labels)
    print(f"✅ Training Complete! Model accuracy on training set: {model.score(texts, labels):.2f}")

    # Save the trained model artifact to your local machine
    os.makedirs("backend/ml/artifacts", exist_ok=True)
    with open("backend/ml/artifacts/router_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("💾 Router Model saved to backend/ml/artifacts/router_model.pkl")

if __name__ == "__main__":
    train_intent_router()