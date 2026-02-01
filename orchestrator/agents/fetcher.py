from orchestrator.schemas import AnalysisPlan
from data.canonical import IndicatorSeries
from data.adapters.worldbank_adapter import WorldBankAdapter

class FetcherAgent:
    def __init__(self):
        # Initialize our adapters once (Singleton-ish)
        self.wb_adapter = WorldBankAdapter()
        # self.oecd_adapter = OECDAdapter() # Coming in future updates

    def execute_plan(self, plan: AnalysisPlan) -> IndicatorSeries:
        """
        Routes the plan to the specific adapter.
        """
        print(f"[Fetcher] Executing plan for: {plan.source} - {plan.target_country}")
        
        if plan.source == "WORLDBANK":
            # Call the World Bank Adapter we built in Stage 6
            return self.wb_adapter.fetch_data(
                country_code=plan.target_country,
                indicator_code=plan.target_indicator,
                start_year=min(plan.years) if plan.years else 2018,
                end_year=max(plan.years) if plan.years else 2022
            )
        
        elif plan.source == "OECD":
            # Placeholder until we build the OECD Adapter
            raise NotImplementedError("OECD Adapter is not yet connected (Coming Soon).")
            
        else:
            raise ValueError(f"Unknown data source: {plan.source}")