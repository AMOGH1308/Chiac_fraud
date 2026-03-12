import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from agents.ingestion_agent import IngestionAgent
from agents.feature_agent import FeatureAgent
from agents.security_agent import SecurityGuardAgent
from agents.detective_agent import DetectiveAgent
from sklearn.metrics import classification_report, confusion_matrix

class MasterOrchestrator:
    """The Master Controller: Manages dynamic interaction between autonomous agents."""
    def __init__(self, train_path, test_path):
        self.train_path = train_path
        self.test_path = test_path
        
        self.ingestion = IngestionAgent(None)
        self.feature_eng = FeatureAgent()
        self.security = SecurityGuardAgent()
        self.detective = DetectiveAgent()
        self.last_report = "System not yet evaluated."
        
    def run(self, force_train=False):
        print("\n" + "="*50)
        print(" FRAUD PATTERN DETECTOR - AGENTIC PIPELINE")
        print("="*50)
        print("\n>>> Phase 1: Training & Model Synchronization...")
        
        # Check if we can bypass training
        if not force_train and self.feature_eng.load() and self.detective.load():
            print(f"[{self.__class__.__name__}] Dynamic Decision: Pre-trained assets found. Skipping training phase.")
        else:
            if force_train:
                print(f"[{self.__class__.__name__}] Dynamic Decision: Force Train requested.")
            else:
                print(f"[{self.__class__.__name__}] Dynamic Decision: No models found. Initiating full training...")
            
            self.ingestion.filepath = self.train_path
            train_raw = self.ingestion.execute()['data']
            self.feature_eng.fit(train_raw)
            train_processed = self.feature_eng.execute(train_raw)['data']
            self.detective.train(train_processed)
            print(f"[{self.__class__.__name__}] System synchronization complete.")
        
        print("\n>>> Phase 2: Evaluating Against Adversarial Data...")
        self.ingestion.filepath = self.test_path
        test_raw = self.ingestion.execute()['data']
        test_processed = self.feature_eng.execute(test_raw)['data']
        
        security_res = self.security.execute(test_raw)
        detective_res = self.detective.execute(test_processed)
        
        security_scores = security_res['scores']
        detective_probs = detective_res['scores']
        
        # Applying Optimized Thresholds
        HIGH_THRESH = 0.7
        MID_THRESH = 0.3
        SEC_WEIGHT = 0.2
        
        final_pred = []
        for s_score, d_prob in zip(security_scores, detective_probs):
            if s_score > HIGH_THRESH:
                final_pred.append(1)
            elif s_score > MID_THRESH:
                final_pred.append(1 if (SEC_WEIGHT * s_score + (1-SEC_WEIGHT) * d_prob) > 0.5 else 0)
            else:
                final_pred.append(1 if d_prob > 0.5 else 0)
        
        final_pred = np.array(final_pred)
        y_true = test_raw['is_fraud']
        
        # Ensure reports directory exists
        if not os.path.exists('reports'):
            os.makedirs('reports')
            # Save Visual Reports (Confusion Matrix & Feature Importance)
        self.generate_reports(y_true, final_pred, test_processed)
        
        report_text = classification_report(y_true, final_pred)
        self.last_report = report_text # Store for UI access
        
        print("\n" + "#"*40)
        print(" ADVERSARIAL TEST REPORT")
        print("#"*40)
        print(report_text)
        
        accuracy = (final_pred == y_true).mean()
        print(f"System Performance on Adversarial Data: {accuracy*100:.2f}%")
        print("="*50 + "\n")
        return report_text

    def generate_reports(self, y_true, y_pred, df_processed):
        # 1. Confusion Matrix
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens')
        plt.title('System Decision Confidence Matrix')
        plt.savefig('reports/confusion_matrix.png')
        plt.close()
        
        # 2. Feature Importance
        if hasattr(self.detective.model, 'feature_importances_'):
            X = df_processed.drop(['is_fraud'], axis=1, errors='ignore')
            importances = self.detective.model.feature_importances_
            feat_importances = pd.Series(importances, index=X.columns)
            plt.figure(figsize=(10, 6))
            feat_importances.nlargest(10).plot(kind='barh', color='darkblue')
            plt.title('Agent Predictive Influence (Feature Importance)')
            plt.savefig('reports/feature_importance.png')
            plt.close()
        print(f"[{self.__class__.__name__}] Analytic assets updated in /reports/")

    def predict_single(self, transaction_dict):
        """Method for Streamlit UI: Predicts fraud and collects agentic logs."""
        logs = []
        df_raw = pd.DataFrame([transaction_dict])
        
        # 1. Ingestion Audit
        logs.append(f"[IngestionAgent] Validating input data components...")
        
        # 2. Feature Transformation
        res_feat = self.feature_eng.execute(df_raw)
        df_proc = res_feat['data']
        logs.append(f"[FeatureAgent] {res_feat.get('reasoning', 'Features processed.')}")
        
        # 3. Level 1 Audit
        res_sec = self.security.execute(df_raw)
        s_score = res_sec['scores'][0]
        logs.append(f"[SecurityGuardAgent] {res_sec.get('reasoning', 'Audit complete.')}")
        
        # --- AGENTIC DECISION WATERFALL ---
        
        # Case A: Security Override (High Risk)
        if s_score > 0.7:
            logs.append(f"[Orchestrator] High Risk Detected ({s_score:.2f}). Security Override active.")
            return {
                "verdict": "FRAUD",
                "reason": "Security Override: High-risk rule violation detected. (Detective not needed)",
                "security_score": s_score,
                "detective_prob": 0.0,
                "triggered_detective": False,
                "logs": logs
            }
            
        # Characterize the transition to Detective
        if s_score > 0.3:
            logs.append(f"[Orchestrator] Mid-Risk Patterns ({s_score:.2f}). Seeking Detective consensus...")
        else:
            logs.append(f"[Orchestrator] Low-Risk Baseline ({s_score:.2f}). Deep ML verification initiated...")
            
        res_det = self.detective.execute(df_proc)
        d_prob = res_det['scores'][0]
        logs.append(f"[DetectiveAgent] {res_det.get('reasoning', 'Pattern analysis complete.')}")
        
        verdict = "SAFE"
        reason = "System consensus: Transaction is safe."
        
        if s_score > 0.3:
            if (0.2 * s_score + 0.8 * d_prob) > 0.5:
                verdict = "FRAUD"
                reason = "Hybrid Analysis: Combined risk indicators exceed threshold."
            else:
                reason = "Hybrid Analysis: Suspicious, but combined risk is manageable."
        else:
            if d_prob > 0.5:
                verdict = "FRAUD"
                reason = "Detective ML: High probability of hidden fraud patterns spotted."
        
        logs.append(f"[Orchestrator] Waterfall decision: {verdict}. Reasoning: {reason}")
        
        return {
            "verdict": verdict,
            "reason": reason,
            "security_score": s_score,
            "detective_prob": d_prob,
            "triggered_detective": True,
            "logs": logs
        }
