import os
import pickle
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

def train_intent_router():
    print("⏳ Downloading the official Banking77 dataset via Hugging Face...")
    dataset = load_dataset("banking77")
    train_data = dataset["train"]

    def map_to_agent(label_id):
        label_name = train_data.features["label"].names[label_id]
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

    print("⚙️ Processing banking data...")
    texts = list(train_data["text"])
    labels = [map_to_agent(label_id) for label_id in train_data["label"]]

    # --- NEW: Inject Domain-Specific TechMart Data ---
    print("💉 Injecting custom TechMart e-commerce and electronics data...")
    custom_texts = [
        # Technical Support Examples
        "My smart home hub keeps disconnecting from the Wi-Fi. How do I factory reset it?",
        "I am trying to install the TechMart software on my Windows 11 machine, but the installation crashes at 90%.",
        "I can't log into my account. It keeps giving me an 'Error 404' every time I enter my password.",
        "The screen on my laptop is flickering and the battery won't charge.",
        "How do I update the firmware on my wireless router?",
        "My bluetooth is not connecting to my phone.",
        
        # Product Examples
        "Is the new wireless gaming headset compatible with the PlayStation 5?",
        "What is the difference between the standard TechMart laptop and the Pro version?",
        "Does the Pro laptop have a dedicated GPU?",
        "What are the battery life specifications for your portable solar charger?",
        "Do you have the iPhone 15 in stock in blue?",
        "How much RAM does this motherboard support?"
    ]
    
    custom_labels = [
        "technical", "technical", "technical", "technical", "technical", "technical",
        "product", "product", "product", "product", "product", "product"
    ]
    
    # We heavily multiply the custom data so it isn't drowned out by the 10,000 banking rows
    texts.extend(custom_texts * 50) 
    labels.extend(custom_labels * 50)

    print("🧠 Training the Machine Learning Router Pipeline...")
    model = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_features=5000),
        # Added class_weight="balanced" to handle the dataset imbalance
        LogisticRegression(solver='lbfgs', max_iter=1000, class_weight="balanced") 
    )
    
    model.fit(texts, labels)
    print(f"✅ Training Complete! Model accuracy on training set: {model.score(texts, labels):.2f}")

    os.makedirs("backend/ml/artifacts", exist_ok=True)
    with open("backend/ml/artifacts/router_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("💾 Router Model saved to backend/ml/artifacts/router_model.pkl")

if __name__ == "__main__":
    train_intent_router()