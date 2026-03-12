import streamlit as st
import pandas as pd
import os
from main_orchestrator import MasterOrchestrator

# --- Page Configuration ---
st.set_page_config(page_title="Agentic Fraud Detector", layout="wide")

# --- Initialize Orchestrator ---
@st.cache_resource
def get_orchestrator():
    orch = MasterOrchestrator('advanced_fraud_data.csv', 'adversarial_test_data.csv')
    orch.run()
    return orch

orchestrator = get_orchestrator()

# --- Sidebar ---
st.sidebar.title("🔍 Fraud Intelligence")
st.sidebar.info("Agentic Pipeline: Security Guard (Rules) + Detective (ML)")

if st.sidebar.button("Refresh System Analytics"):
    orchestrator.run(force_train=True)
    st.sidebar.success("Retrained & Updated!")

# --- Main Dashboard ---
st.title("🛡️ Agentic Fraud Pattern Detector")
st.markdown("---")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📝 Transaction Audit")
    
    amt = st.number_input("Transaction Amount ($)", min_value=0.0, value=150.0)
    category = st.selectbox("Category", ['misc_net', 'travel', 'gas_transport', 'grocery_pos', 'shopping_net', 'entertainment'])
    merchant = st.selectbox("Merchant Name", ['Starbucks', 'Steam', 'Amazon', 'Chevron', 'Walmart', 'Unknown_Foreign_Store', 'Delta Air'])
    payment_method = st.selectbox("Payment Method", ['Credit_Card', 'Digital_Wallet', 'Debit_Card', 'Wire_Transfer'])
    distance_km = st.number_input("Distance from Home (km)", min_value=0.0, value=10.0)
    hour = st.slider("Hour of Day", 0, 23, 12)
    is_international = st.checkbox("International Transaction")
    
    # UI Logic: CVV only applies to Cards
    is_card = payment_method in ['Credit_Card', 'Debit_Card']
    cvv_matches = st.checkbox("CVV Matches", value=True, disabled=not is_card, help="Only relevant for Credit/Debit cards.")
    
    submit = st.button("Run Agentic Audit")

    if submit:
        # Prepare input for agent
        tx_data = {
            "amt": amt, "category": category, "merchant": merchant,
            "payment_method": payment_method, "distance_km": distance_km,
            "hour": hour, "is_international": 1 if is_international else 0,
            "cvv_matches": 1 if cvv_matches else 0, "is_fraud": 0
        }
        
        with st.spinner("Agents are analyzing..."):
            result = orchestrator.predict_single(tx_data)
            
        st.markdown("### 📢 Agent Verdict")
        if result['verdict'] == "FRAUD":
            st.error(f"**RESULT: REJECTED**")
            st.write(f"### 🚨 {result['reason']}")
        else:
            st.success(f"**RESULT: APPROVED**")
            st.write(f"### ✅ {result['reason']}")
            
        st.write(f"**Security Guard Risk Score:** `{result.get('security_score', 0):.2f}`")
        
        if result.get('triggered_detective', False):
            st.write(f"**Detective ML Probability:** `{result.get('detective_prob', 0):.2f}`")
        else:
            st.info("💡 **Note:** The Detective was skipped because the Security Guard caught a clear violation early.")

with col2:
    st.subheader("📊 System Intelligence Reports")
    tabs = st.tabs(["Performance", "Predictive Factors", "Agent Logs"])
    
    with tabs[0]:
        st.markdown("#### System Confidence Matrix")
        if os.path.exists('reports/confusion_matrix.png'):
            st.image('reports/confusion_matrix.png', use_container_width=True)
            
            st.markdown("#### Adversarial Classification Report")
            if hasattr(orchestrator, 'last_report'):
                st.code(orchestrator.last_report, language="text")
            else:
                st.info("Run system analytics to view metrics.")
        else:
            st.warning("No performance report found.")
            
    with tabs[1]:
        st.markdown("#### Agent Influence (Feature Importance)")
        if os.path.exists('reports/feature_importance.png'):
            st.image('reports/feature_importance.png', use_container_width=True)
            
    with tabs[2]:
        st.markdown("#### Real-time Agentic Reasoning")
        if submit and 'result' in locals() and 'logs' in result:
            st.code("\n".join(result['logs']), language="text")
        else:
            st.info("Run an audit to see real-time agent logs.")

st.markdown("---")
st.caption("Agentic Fraud Detection System v2.2 | Final Revert State")
