import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import joblib
import os

class FeatureAgent:
    """Agent B: Autonomous entity for transforming raw data into intelligence."""
    def __init__(self, model_dir='models'):
        self.le = {col: LabelEncoder() for col in ['category', 'merchant', 'payment_method']}
        self.scaler = MinMaxScaler()
        self.is_fitted = False
        self.model_dir = model_dir
        self.save_path = os.path.join(self.model_dir, 'feature_assets.joblib')
        
    def fit(self, df):
        print(f"[{self.__class__.__name__}] Learning data patterns (fitting)...")
        for col, encoder in self.le.items():
            encoder.fit(df[col])
        self.scaler.fit(df[['amt', 'distance_km']])
        self.is_fitted = True
        self.save()

    def save(self):
        """Persist fitting assets to disk."""
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
        assets = {
            'le': self.le,
            'scaler': self.scaler
        }
        joblib.dump(assets, self.save_path)
        print(f"[{self.__class__.__name__}] Assets persisted to {self.save_path}")

    def load(self):
        """Load persisted assets from disk."""
        if os.path.exists(self.save_path):
            assets = joblib.load(self.save_path)
            self.le = assets['le']
            self.scaler = assets['scaler']
            self.is_fitted = True
            print(f"[{self.__class__.__name__}] Assets loaded from {self.save_path}")
            return True
        return False

    def execute(self, df):
        print(f"[{self.__class__.__name__}] Transforming features for processing...")
        if df is None or df.empty:
            return {"status": "ERROR", "message": "No data provided"}
            
        if not self.is_fitted:
            if not self.load():
                print(f"[{self.__class__.__name__}] Warning: No persisted assets found. Fitting on current data.")
                self.fit(df)
            
        df_processed = df.copy()
        
        # Categorical Transformation
        for col, encoder in self.le.items():
            try:
                df_processed[col] = encoder.transform(df_processed[col])
            except ValueError:
                print(f"[{self.__class__.__name__}] Warning: Unseen labels in {col}. Re-fitting (Adaptive Mode).")
                df_processed[col] = encoder.fit_transform(df_processed[col])
            
        # Numerical Scaling
        df_processed[['amt', 'distance_km']] = self.scaler.transform(df_processed[['amt', 'distance_km']])
        
        # Temporal Logic
        df_processed['is_late_night'] = ((df_processed['hour'] >= 1) & (df_processed['hour'] <= 5)).astype(int)
        
        reasoning = "Normalization and Label Encoding complete. Temporal features engineered."
        print(f"[{self.__class__.__name__}] Decision: {reasoning}")
        return {"status": "SUCCESS", "data": df_processed, "reasoning": reasoning}
