import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

class DetectiveAgent:
    """Layer 2 Agent: Autonomous ML predictive engine."""
    def __init__(self, model_dir='models'):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.model_dir = model_dir
        self.save_path = os.path.join(self.model_dir, 'detective_model.joblib')
        
    def train(self, df):
        print(f"[{self.__class__.__name__}] Upskilling: Training internal model...")
        X = df.drop(['is_fraud'], axis=1)
        y = df['is_fraud']
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        self.save()
        print(f"[{self.__class__.__name__}] Training complete.")

    def save(self):
        """Persist model to disk."""
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
        joblib.dump(self.model, self.save_path)
        print(f"[{self.__class__.__name__}] Model persisted to {self.save_path}")

    def load(self):
        """Load persisted model from disk."""
        if os.path.exists(self.save_path):
            self.model = joblib.load(self.save_path)
            self.is_trained = True
            print(f"[{self.__class__.__name__}] Model loaded from {self.save_path}")
            return True
        return False

    def execute(self, df):
        print(f"[{self.__class__.__name__}] Investigating patterns using ML brain...")
        if not self.is_trained:
            if not self.load():
                return {"status": "ERROR", "message": "Model not trained and no persisted model found"}
            
        X = df.drop(['is_fraud'], axis=1, errors='ignore')
        probs = self.model.predict_proba(X)[:, 1]
        avg_prob = np.mean(probs)
        
        reasoning = f"ML Brain analysis complete. Identified {avg_prob*100:.1f}% probability of advanced fraud patterns."
        print(f"[{self.__class__.__name__}] Decision: {reasoning}")
        return {"status": "SUCCESS", "scores": probs, "reasoning": reasoning}
