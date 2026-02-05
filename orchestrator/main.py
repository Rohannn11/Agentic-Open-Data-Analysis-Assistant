# ... Imports ...
from orchestrator.agents.planner import PlannerAgent # Smart Planner
from orchestrator.agents.fetcher import FetcherAgent
from orchestrator.agents.analyst import AnalystAgent
from orchestrator.agents.narrator import NarratorAgent

class AgentOrchestrator:
    def __init__(self):
        # We REMOVED self.router because Planner now does the thinking
        self.planner = PlannerAgent()
        self.fetcher = FetcherAgent()
        self.analyst = AnalystAgent()
        self.narrator = NarratorAgent()

    def run_pipeline(self, user_query: str):
        try:
            # 1. SMART PLANNING (Replaces Router + Old Planner)
            # Gemini decides Source + Indicator here
            plan = self.planner.create_plan(user_query)
            
            # 2. Fetching (Supports OECD now)
            raw_data = self.fetcher.execute_plan(plan)
            
            # 3. Analysis
            stats = self.analyst.analyze(raw_data)
            
            # 4. Narration
            narrative = self.narrator.summarize(
                plan.target_country, plan.target_indicator, stats.model_dump()
            )
            
            return {
                "type": "success",
                "data": {
                    "source": plan.source, # See which one Gemini picked!
                    "narrative": narrative,
                    "analysis": stats.model_dump()
                }
            }
        except Exception as e:
            return {"type": "error", "message": str(e)}