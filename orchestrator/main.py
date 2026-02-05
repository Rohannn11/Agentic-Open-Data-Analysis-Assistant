# ... Imports ...
from orchestrator.agents.planner import PlannerAgent # Smart Planner
from orchestrator.agents.fetcher import FetcherAgent
from orchestrator.agents.analyst import AnalystAgent
from orchestrator.agents.narrator import NarratorAgent
from orchestrator.logger import get_logger # <--- NEW IMPORT

logger = get_logger("Orchestrator")

class AgentOrchestrator:
    def __init__(self):
        # We REMOVED self.router because Planner now does the thinking
        self.planner = PlannerAgent()
        self.fetcher = FetcherAgent()
        self.analyst = AnalystAgent()
        self.narrator = NarratorAgent()

def run_pipeline(self, user_query: str):
        logger.info(f"Starting pipeline for query: {user_query}")
        
        try:
            # 1. Planning
            plan = self.planner.create_plan(user_query)
            logger.info(f"Plan created: Source={plan.source}, Countries={plan.target_countries}")
            
            # 2. Fetching
            raw_data_list = self.fetcher.execute_plan(plan)
            logger.info(f"Fetching complete. Retrieved {len(raw_data_list)} datasets.")
            
            # 3. Analysis
            stats = self.analyst.analyze(raw_data_list)
            
            # 4. Narration
            narrative = self.narrator.summarize(
                country=plan.target_countries,
                indicator=plan.target_indicators,
                stats=stats.model_dump()
            )
            
            logger.info("Pipeline executed successfully.")
            
            return {
                "type": "success",
                "data": {
                    "source": plan.source,
                    "narrative": narrative,
                    "analysis": stats.model_dump()
                }
            }
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            return {"type": "error", "message": str(e)}