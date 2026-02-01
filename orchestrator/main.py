import uuid
from datetime import datetime
# Import ALL agents
from orchestrator.agents.dataset_router import DatasetRouterAgent
from orchestrator.agents.planner import PlannerAgent
from orchestrator.agents.fetcher import FetcherAgent
from orchestrator.agents.analyst import AnalystAgent
from orchestrator.agents.narrator import NarratorAgent

class AgentOrchestrator:
    def __init__(self):
        self.version = "1.0.0"
        
        # --- INITIALIZE ALL TOOLS ---
        self.router = DatasetRouterAgent()
        self.planner = PlannerAgent()
        self.fetcher = FetcherAgent()
        self.analyst = AnalystAgent()
        self.narrator = NarratorAgent()

    def run_pipeline(self, user_query: str):
        print(f"[Orchestrator] Starting pipeline for: {user_query}")
        
        try:
            # 1. Routing
            selected_sources = self.router.determine_source(user_query)
            primary_source = selected_sources[0]
            
            # 2. Planning
            plan = self.planner.create_plan(user_query, primary_source)
            
            # 3. Fetching
            raw_data = self.fetcher.execute_plan(plan)
            
            # 4. Analysis
            stats = self.analyst.analyze(raw_data)
            stats_dict = stats.model_dump()
            
            # 5. Narration (Gemini)
            narrative = self.narrator.summarize(
                country=plan.target_country,
                indicator=plan.target_indicator,
                stats=stats_dict
            )
            
            # --- FINAL RESPONSE ---
            return {
                "type": "orchestrator_response",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "query": user_query,
                    "source": primary_source,
                    "analysis": stats_dict,
                    "narrative": narrative
                }
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "type": "error",
                "message": str(e)
            }