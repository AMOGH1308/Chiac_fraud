# Agentic Fraud Pattern Detector

An advanced, multi-agentic system designed to identify and flag fraudulent transactions using a hybrid approach of deterministic security rules and machine learning predictive modeling. Now featuring an interactive Streamlit dashboard for real-time transaction auditing.

## 🚀 Overview

This project implements a **Dynamic Multi-Agent System** where specialized agents collaborate to analyze transaction data in real-time. By combining a "Security Guard" (rule-based) with a "Detective" (Random Forest ML), the system achieves high precision in detecting fraudulent patterns. The system includes an interactive web interface for manual auditing and simulation.

## 🏗️ Architecture

The system follows an **Agentic Pipeline** architecture:

- **Ingestion Agent**: Sources and validates raw transaction data.
- **Feature Agent**: Performs autonomous feature engineering and normalization.
- **Security Guard Agent (Layer 1)**: Executes high-confidence deterministic rules.
- **Detective Agent (Layer 2)**: Analyzes non-linear patterns using Random Forest.
- **Master Orchestrator**: Coordinates the cross-agent communication and final decision logic.

## 📂 Project Structure

```text
/
├── app.py                    # Streamlit Interactive Dashboard
├── main_orchestrator.py      # Core Project Hub & Agent Launcher
├── advanced_fraud_data.csv   # Training Dataset
├── adversarial_test_data.csv # Test Dataset for Verification
├── requirements.txt         # Project dependencies
├── agents/                  # Autonomous Agent modules
│   ├── ingestion_agent.py
│   ├── feature_agent.py
│   ├── security_agent.py
│   └── detective_agent.py
├── models/                  # Persisted ML models and assets
└── reports/                 # Generated analytic reports
```

## 🛠️ Setup & Execution

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Interactive Dashboard**:
   ```bash
   streamlit run app.py
   ```

3. **Run the Backend Evaluation**:
   ```bash
   python main_orchestrator.py
   ```

## 📊 Performance Metrics

The system is evaluated against adversarial data to ensure robustness:

| Metric | Target Value |
| :--- | :--- |
| **Precision** | **~1.00** |
| **Recall** | **~1.00** |
| **Accuracy** | **~99-100%** |
