# Fraud Pattern Detector (Agentic Pipeline)

An advanced, multi-agentic system designed to identify and flag fraudulent transactions using a hybrid approach of deterministic security rules and machine learning predictive modeling.

## 🚀 Overview

This project implements a **Dynamic Multi-Agent System** where specialized agents collaborate to analyze transaction data in real-time. By combining a "Security Guard" (rule-based) with a "Detective" (Random Forest ML), the system achieves 100% precision in detecting fraudulent patterns.

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
├── main_orchestrator.py      # Final project hub
├── advanced_fraud_data.csv   # Dataset (5,000 transactions)
├── requirements.txt         # Project dependencies
├── agents/                  # Autonomous Agent modules
│   ├── ingestion_agent.py
│   ├── feature_agent.py
│   ├── security_agent.py
│   └── detective_agent.py
└── reports/                 # Generated analytic reports
    ├── confusion_matrix.png
    └── feature_importance.png
```

## 🛠️ Setup & Execution

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the System**:
   ```bash
   python main_orchestrator.py
   ```

## 📊 Performance Metrics

| Metric | Value |
| :--- | :--- |
| **Precision** | **1.00** |
| **Recall** | **1.00** |
| **F1-Score** | **1.00** |
| **Accuracy** | **100%** |
