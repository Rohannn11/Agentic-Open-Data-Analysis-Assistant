import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from orchestrator.schemas import AnalysisPlan
from orchestrator.logger import get_logger

load_dotenv()
logger = get_logger("PlannerAgent")

class PlannerAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.critical("GEMINI_API_KEY is missing!")
            raise ValueError("GEMINI_API_KEY required for Planner")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def create_plan(self, query: str) -> AnalysisPlan:
        logger.info(f"Designing plan for query: '{query}'")

        prompt = f"""
        You are an Expert Data Planner.
        USER QUERY: "{query}"

        AVAILABLE METRICS:
        1. WORLDBANK:
           - GDP Growth: "NY.GDP.MKTP.KD.ZG"
           - Inflation: "FP.CPI.TOTL.ZG"
           - Population: "SP.POP.TOTL"
           - CO2 Emissions: "EN.ATM.CO2E.KT"
        2. OECD:
           - Unemployment Rate: "HUR"
           - Hourly Earnings: "EARNINGS"

        INSTRUCTIONS:
        1. Extract ALL countries (ISO 3-letter codes). Default to ["USA"] if none.
        2. Determine primary indicator code.
        3. Context Rule: If GDP/Unemployment is asked, ALWAYS add "FP.CPI.TOTL.ZG" (Inflation) as secondary.
        4. Select Source (WORLDBANK or OECD).

        RETURN JSON ONLY:
        {{
            "target_countries": ["IND", "USA"],
            "target_indicators": ["PRIMARY_CODE", "CONTEXT_CODE"],
            "source": "WORLDBANK", 
            "topic": "economic_analysis"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            clean_json = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)

            logger.info(f"AI Plan Generated: {data}")

            return AnalysisPlan(
                original_query=query,
                source=data["source"],
                topic=data["topic"],
                target_countries=data["target_countries"],
                target_indicators=data["target_indicators"],
                years=[2018, 2019, 2020, 2021, 2022]
            )

        except Exception as e:
            logger.error(f"Planning failed: {e}", exc_info=True)
            # Fallback
            return AnalysisPlan(
                original_query=query, source="WORLDBANK", topic="error_fallback",
                target_countries=["USA"], target_indicators=["NY.GDP.MKTP.KD.ZG"], 
                years=[2020, 2021, 2022]
            )