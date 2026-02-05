from typing import List
from orchestrator.schemas import AnalysisPlan
from data.canonical import IndicatorSeries
from data.adapters.worldbank_adapter import WorldBankAdapter
from data.adapters.oecd_adapter import OECDAdapter

class FetcherAgent:
    def __init__(self):
        self.wb_adapter = WorldBankAdapter()
        self.oecd_adapter = OECDAdapter()

    def execute_plan(self, plan: AnalysisPlan) -> List[IndicatorSeries]:
        results = []
        
        # Double Loop: Countries x Indicators
        for country in plan.target_countries:
            for indicator in plan.target_indicators:
                try:
                    if plan.source == "WORLDBANK":
                        data = self.wb_adapter.fetch_data(
                            country, indicator, min(plan.years), max(plan.years)
                        )
                    elif plan.source == "OECD":
                        data = self.oecd_adapter.fetch_data(
                            country, indicator, min(plan.years), max(plan.years)
                        )
                    else:
                        continue 
                    
                    if data.data:
                        results.append(data)

                except Exception as e:
                    print(f"[Fetcher] Error fetching {country}-{indicator}: {e}")
                    
        return results