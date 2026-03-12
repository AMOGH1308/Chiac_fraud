import pandas as pd

class IngestionAgent:
    """Agent A: Autonomous entity for sourcing data."""
    def __init__(self, filepath):
        self.filepath = filepath
        
    def execute(self):
        print(f"[{self.__class__.__name__}] Investigating data source: {self.filepath}")
        try:
            df = pd.read_csv(self.filepath)
            reasoning = f"Data validation successful. Sourced from {self.filepath}."
            print(f"[{self.__class__.__name__}] Decision: {reasoning}")
            return {"status": "SUCCESS", "data": df, "reasoning": reasoning}
        except Exception as e:
            reasoning = f"Source unavailable: {str(e)}"
            print(f"[{self.__class__.__name__}] Decision: {reasoning}")
            return {"status": "ERROR", "message": str(e), "reasoning": reasoning}
