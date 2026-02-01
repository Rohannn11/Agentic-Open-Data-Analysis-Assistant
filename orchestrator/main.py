import uuid
from datetime import datetime
from orchestrator.agents.dataset_router import DatasetRouterAgent
from orchestrator.agents.planner import PlannerAgent
from orchestrator.agents.fetcher import FetcherAgent
from orchestrator.agents.analyst import AnalystAgent # <--- NEW IMPORT

class AgentOrchestrator:
    def __init__(self):
        self.version = "1.0.0"
        self.router = DatasetRouterAgent()
        self.planner = PlannerAgent()
        self.fetcher = FetcherAgent()
        self.analyst = AnalystAgent()       # <--- NEW TOOL

    def run_pipeline(self, user_query: str):
        print(f"[Orchestrator] Starting pipeline for: {user_query}")
        
        try:
            # 1. Routing
            selected_sources = self.router.determine_source(user_query)
            primary_source = selected_sources[0]
            
            # 2. Planning
            plan = self.planner.create_plan(user_query, primary_source)
            
            # 3. Fetching (Raw Data)
            raw_data = self.fetcher.execute_plan(plan)
            
            # --- STAGE 8: ANALYSIS (The New Step) ---
            # Turn raw numbers into insights
            stats = self.analyst.analyze(raw_data)
            
            # --- CONSTRUCT FINAL RESPONSE ---
            return {
                "type": "orchestrator_response",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "query": user_query,
                    "plan": plan.model_dump(),
                    "raw_data_points": len(raw_data.data), # Just showing count for brevity
                    "analysis": stats.model_dump(),        # <--- THE INSIGHTS
                    "next_step": "LLM Narration (Stage 9)"
                }
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "type": "error",
                "message": str(e)
            }