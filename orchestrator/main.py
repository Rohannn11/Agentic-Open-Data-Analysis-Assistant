from orchestrator.agents.planner import PlannerAgent
from orchestrator.agents.fetcher import FetcherAgent
from orchestrator.agents.analyst import AnalystAgent
from orchestrator.agents.narrator import NarratorAgent
from orchestrator.logger import get_logger

# Initialize Logger
logger = get_logger("Orchestrator")

class AgentOrchestrator:
    def __init__(self):
        logger.info("Initializing Agent Orchestrator...")
        self.planner = PlannerAgent()
        self.fetcher = FetcherAgent()
        self.analyst = AnalystAgent()
        self.narrator = NarratorAgent()
        logger.info("All agents initialized successfully.")

    def run_pipeline(self, user_query: str):
        logger.info(f"Received Query: {user_query}")
        
        try:
            # 1. Planning
            plan = self.planner.create_plan(user_query)
            logger.info(f"Plan Created | Source: {plan.source} | Targets: {plan.target_countries}")
            
            # 2. Fetching
            raw_data_list = self.fetcher.execute_plan(plan)
            logger.info(f"Fetching Complete | Datasets Retrieved: {len(raw_data_list)}")
            
            # 3. Analysis
            stats = self.analyst.analyze(raw_data_list)
            logger.info(f"Analysis Complete | Trend: {stats.trend_direction}")
            
            # 4. Narration
            narrative = self.narrator.summarize(
                country=plan.target_countries,
                indicator=plan.target_indicators,
                stats=stats.model_dump()
            )
            logger.info("Narration Generated.")
            
            return {
                "type": "success",
                "data": {
                    "source": plan.source,
                    "narrative": narrative,
                    "analysis": stats.model_dump()
                }
            }
        except Exception as e:
            logger.error(f"Pipeline Critical Failure: {str(e)}", exc_info=True)
            return {"type": "error", "message": str(e)}