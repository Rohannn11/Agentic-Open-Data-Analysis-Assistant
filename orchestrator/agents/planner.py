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
        1. **Extraction**: Identify ALL countries mentioned. Convert to ISO 3-letter codes.
        2. **Validation**: If NO country is found, set "target_countries" to [].
        3. **Indicators**: Pick the most relevant indicator code.
        4. **Context**: If GDP/Unemployment is asked, ALWAYS add "FP.CPI.TOTL.ZG" (Inflation) as secondary.
        5. **Source**: Choose WORLDBANK or OECD.

        RETURN JSON ONLY:
        {{
            "target_countries": ["ISO_CODE_1", "ISO_CODE_2"], 
            "target_indicators": ["PRIMARY_CODE", "CONTEXT_CODE"],
            "source": "WORLDBANK_OR_OECD", 
            "topic": "economic_analysis"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            clean_json = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)

            logger.info(f"AI Plan Generated: {data}")

            # VALIDATION CHECK
            # If the AI couldn't find any countries, we shouldn't default to USA.
            # We should tell the user to be more specific.
            if not data.get("target_countries"):
                raise ValueError("No valid countries found in query. Please mention a country (e.g., 'India', 'France').")

            return AnalysisPlan(
                original_query=query,
                source=data["source"],
                topic=data["topic"],
                target_countries=data["target_countries"],
                target_indicators=data["target_indicators"],
                years=[2018, 2019, 2020, 2021, 2022]
            )

        except json.JSONDecodeError:
            logger.error("Planner failed to parse AI response.")
            raise ValueError("System Error: Planner AI returned invalid JSON. Please try again.")
            
        except Exception as e:
            logger.error(f"Planning failed: {e}", exc_info=True)
            # STOP THE FALLBACK. Raise the error so the Frontend sees it.
            raise ValueError(f"Could not plan query: {str(e)}")