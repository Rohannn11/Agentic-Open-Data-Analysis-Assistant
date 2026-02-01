import uuid
from datetime import datetime
from orchestrator.agents.dataset_router import DatasetRouterAgent # <--- IMPORT

class AgentOrchestrator:
    def __init__(self):
        self.version = "1.0.0"
        # Initialize our tools
        self.router = DatasetRouterAgent()

    def run_pipeline(self, user_query: str):
        """
        The Core Logic:
        1. Router (Stage 4) -> Decide Source
        """
        print(f"[Orchestrator] Starting pipeline for: {user_query}")
        
        # --- STAGE 4: ROUTING ---
        # Ask the router which API to use
        selected_sources = self.router.determine_source(user_query)
        print(f"[Orchestrator] Router selected: {selected_sources}")

        # --- RESPONSE ---
        return {
            "type": "orchestrator_response",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "original_query": user_query,
                "step_1_routing": {
                    "selected_sources": selected_sources,
                    "reason": "Keyword matched in deterministic router"
                },
                "next_step": "Planning (Stage 5)"
            }
        }