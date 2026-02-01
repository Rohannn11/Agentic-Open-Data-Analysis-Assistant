import uuid
from datetime import datetime
from orchestrator.agents.dataset_router import DatasetRouterAgent
from orchestrator.agents.planner import PlannerAgent  # <--- NEW IMPORT

class AgentOrchestrator:
    def __init__(self):
        self.version = "1.0.0"
        self.router = DatasetRouterAgent()
        self.planner = PlannerAgent()       # <--- NEW TOOL

    def run_pipeline(self, user_query: str):
        print(f"[Orchestrator] Starting pipeline for: {user_query}")
        
        try:
            # --- STAGE 4: ROUTING ---
            selected_sources = self.router.determine_source(user_query)
            primary_source = selected_sources[0] # Pick the first one
            print(f"[Orchestrator] Router selected: {primary_source}")

            # --- STAGE 5: PLANNING ---
            # We pass the Router's decision to the Planner
            plan = self.planner.create_plan(user_query, primary_source)
            print(f"[Orchestrator] Plan created: {plan.target_country} -> {plan.target_indicator}")

            return {
                "type": "orchestrator_response",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "stage_4_source": primary_source,
                    "stage_5_plan": plan.model_dump(), # Convert Pydantic to JSON
                    "next_step": "Data Fetching (Stage 7)"
                }
            }
            
        except ValueError as e:
            # This handles your "irrelevant query" question!
            return {
                "type": "error",
                "message": str(e),
                "suggestion": "Try asking about 'GDP' or 'Unemployment'."
            }