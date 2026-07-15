import os
import pickle

class IntentRouter:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "../ml/artifacts/router_model.pkl")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError("❌ Trained router model missing! Run train_router.py first.")
            
        # Load your custom Machine Learning pipeline
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def route_query(self, query: str) -> dict:
        """Uses your local trained classifier to predict the target agent."""
        try:
            # The pipeline automatically handles TF-IDF vectorization and classification
            predicted_agent = self.model.predict([query])[0]
            
            # Get the confidence percentage of the prediction
            confidence = max(self.model.predict_proba([query])[0])
            justification = f"Local ML Classifier matched intent with {round(confidence * 100, 1)}% confidence."
            
            return {
                "selected_agents": [predicted_agent],
                "justification": justification
            }
        except Exception as e:
            print(f"❌ Local routing failure: {str(e)}")
            return {"selected_agents": ["faq"], "justification": "Fallback applied."}

if __name__ == "__main__":
    router = IntentRouter()
    print(router.route_query("I was charged twice for my subscription!"))