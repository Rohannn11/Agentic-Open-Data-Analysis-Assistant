from orchestrator.schemas import AnalysisPlan
from datetime import datetime

class PlannerAgent:
    def __init__(self):
        # 1. KNOWLEDGE BASE (The "Brain")
        # In the future, an LLM replaces this dictionary.
        self.country_map = {
            "india": "IND",
            "usa": "USA",
            "us": "USA",
            "united states": "USA",
            "france": "FRA",
            "china": "CHN",
            "germany": "DEU"
        }
        
        self.indicator_map = {
            # World Bank Codes
            "gdp": "NY.GDP.MKTP.KD.ZG",
            "inflation": "FP.CPI.TOTL.ZG",
            "growth": "NY.GDP.MKTP.KD.ZG",
            
            # OECD Codes (Simplified for learning)
            "unemployment": "HUR", # Harmonized Unemployment Rate
            "earnings": "EARN"
        }

    def create_plan(self, query: str, source: str) -> AnalysisPlan:
        """
        Parses the query to extract Country, Indicator, and Time.
        """
        query_lower = query.lower()
        
        # 1. Extract Country
        detected_country = "USA" # Default
        for name, code in self.country_map.items():
            if name in query_lower:
                detected_country = code
                break
                
        # 2. Extract Indicator
        detected_indicator = None
        detected_topic = "unknown"
        
        for topic, code in self.indicator_map.items():
            if topic in query_lower:
                detected_indicator = code
                detected_topic = topic
                break
        
        # 3. SAFETY NET (The answer to your question!)
        # If we can't find a valid indicator, we reject the plan.
        if not detected_indicator:
            raise ValueError(f"Planner could not identify a supported indicator in: '{query}'")

        # 4. Construct the Plan
        return AnalysisPlan(
            original_query=query,
            source=source,
            topic=detected_topic,
            target_country=detected_country,
            target_indicator=detected_indicator,
            years=[2018, 2019, 2020, 2021, 2022] # Default range for now
        )