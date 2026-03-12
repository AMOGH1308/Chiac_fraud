import numpy as np

class SecurityGuardAgent:
    """Layer 1 Agent: Makes autonomous decisions based on deterministic security rules."""
    def execute(self, df):
        print(f"[{self.__class__.__name__}] Intercepting transactions for security audit...")
        rule_scores = []
        triggered_rules_log = []
        for idx, row in df.iterrows():
            score = 0
            rules = []
            
            # 1. Security Check (Only for card-based payments)
            if row['payment_method'] in ['Credit_Card', 'Debit_Card'] and row.get('cvv_matches') == 0: 
                score += 0.5
                rules.append("CVV mismatch")
            
            # 2. High Amount
            if row['amt'] > 1000: 
                score += 0.6
                rules.append("High amount alert (>$1000)")
            elif row['amt'] > 500: 
                score += 0.3
                rules.append("Unusual amount (>$500)")
            
            # 3. Distance
            if row['distance_km'] > 1000: 
                score += 0.5
                rules.append("Extreme distance (>1000km)")
            if row.get('is_international') == 1: 
                score += 0.4
                rules.append("International transaction")
            
            # 4. Temporal
            if 1 <= row['hour'] <= 4: 
                score += 0.5
                rules.append("Suspicious hour (1-4 AM)")
            
            # 5. Payment Method
            if row['payment_method'] == 'Wire_Transfer': 
                score += 0.4
                rules.append("High-risk payment (Wire Transfer)")
            
            # 6. Merchant
            if 'Foreign' in str(row['merchant']): 
                score += 0.4
                rules.append("Blacklisted merchant substring")
            
            rule_scores.append(min(score, 1.0))
            triggered_rules_log.append(rules if rules else ["Standard audit: No rules triggered"])
            
        risk_array = np.array(rule_scores)
        avg_risk = np.mean(risk_array)
        
        decision = "CONTINUE"
        if avg_risk > 0.8:
            decision = "HALT_IMMEDIATE"
            
        reasoning = f"Audit complete. {'Rules triggered: ' + ', '.join(triggered_rules_log[0]) if triggered_rules_log[0][0] != 'Standard audit: No rules triggered' else 'No immediate rule violations.'}"
        print(f"[{self.__class__.__name__}] Decision: {reasoning}")
        return {"status": "SUCCESS", "scores": risk_array, "decision": decision, "reasoning": reasoning}
