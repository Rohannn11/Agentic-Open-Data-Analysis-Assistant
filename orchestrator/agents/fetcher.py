from orchestrator.schemas import AnalysisPlan
from data.canonical import IndicatorSeries
from data.adapters.worldbank_adapter import WorldBankAdapter
from data.adapters.oecd_adapter import OECDAdapter # <--- NEW

class FetcherAgent:
    def __init__(self):
        self.wb_adapter = WorldBankAdapter()
        self.oecd_adapter = OECDAdapter() # <--- ACTIVATE IT

    def execute_plan(self, plan: AnalysisPlan) -> IndicatorSeries:
        print(f"[Fetcher] Executing plan for: {plan.source} - {plan.target_country}")
        
        if plan.source == "WORLDBANK":
            return self.wb_adapter.fetch_data(
                plan.target_country, plan.target_indicator, 
                min(plan.years), max(plan.years)
            )
        
        elif plan.source == "OECD":
            # NOW IT WORKS
            return self.oecd_adapter.fetch_data(
                plan.target_country, plan.target_indicator, 
                min(plan.years), max(plan.years)
            )
            
        else:
            raise ValueError(f"Unknown source: {plan.source}")