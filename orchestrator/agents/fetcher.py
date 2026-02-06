from typing import List
from orchestrator.schemas import AnalysisPlan
from data.canonical import IndicatorSeries
from data.adapters.worldbank_adapter import WorldBankAdapter
from data.adapters.oecd_adapter import OECDAdapter
from orchestrator.logger import get_logger

logger = get_logger("FetcherAgent")

class FetcherAgent:
    def __init__(self):
        self.wb_adapter = WorldBankAdapter()
        self.oecd_adapter = OECDAdapter()

    def execute_plan(self, plan: AnalysisPlan) -> List[IndicatorSeries]:
        results = []
        logger.info(f"Executing fetch loop for {len(plan.target_countries)} countries and {len(plan.target_indicators)} indicators.")
        
        for country in plan.target_countries:
            for indicator in plan.target_indicators:
                try:
                    logger.debug(f"Fetching {country} - {indicator} from {plan.source}")
                    
                    if plan.source == "WORLDBANK":
                        data = self.wb_adapter.fetch_data(
                            country, indicator, min(plan.years), max(plan.years)
                        )
                    elif plan.source == "OECD":
                        data = self.oecd_adapter.fetch_data(
                            country, indicator, min(plan.years), max(plan.years)
                        )
                    else:
                        logger.warning(f"Unknown source: {plan.source}")
                        continue 
                    
                    if data.data:
                        results.append(data)
                    else:
                        logger.warning(f"No data returned for {country} - {indicator}")

                except Exception as e:
                    logger.error(f"Fetch Error [{country}-{indicator}]: {e}")
                    
        return results