import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from orchestrator.schemas import AnalysisPlan

load_dotenv()

class PlannerAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY required for Smart Planner")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def create_plan(self, query: str) -> AnalysisPlan:
        """
        Uses Gemini to intelligently extract Country, Topic, Source, and Indicator Code.
        """
        print(f"[Planner] Asking Gemini to structure query: '{query}'")

        # --- THE INTELLIGENT PROMPT ---
        # We give the LLM our "Menu" of available indicators and sources.
        # It picks the best match based on MEANING, not just keywords.
        prompt = f"""
        You are a Data Query Planner. 
        Your job is to map a user's natural language question to a specific database API.

        USER QUERY: "{query}"

        AVAILABLE DATA SOURCES & INDICATORS:
        1. SOURCE: "WORLDBANK"
           - GDP Growth (Annual %): "NY.GDP.MKTP.KD.ZG"
           - Inflation (CPI): "FP.CPI.TOTL.ZG"
           - Population Total: "SP.POP.TOTL"
           - CO2 Emissions: "EN.ATM.CO2E.KT"

        2. SOURCE: "OECD"
           - Unemployment Rate (HUR): "HUR"
           - Hourly Earnings: "EARNINGS"
           - Consumer Confidence: "CCI"

        INSTRUCTIONS:
        1. Identify the Target Country (Convert to ISO 3-letter code, e.g., India -> IND, USA -> USA).
        2. Identify the most relevant Indicator Code from the list above. 
        3. If the query is vague (e.g., "economic health"), pick the best proxy (like GDP).
        4. Select the correct Source (WORLDBANK or OECD) based on the indicator.
        5. Return ONLY a valid JSON object.

        JSON FORMAT:
        {{
            "target_country": "IND",
            "target_indicator": "NY.GDP.MKTP.KD.ZG",
            "source": "WORLDBANK",
            "topic": "gdp_growth"
        }}
        """

        try:
            # 1. Ask Gemini
            response = self.model.generate_content(prompt)
            
            # 2. Clean and Parse JSON
            # Gemini might wrap code in ```json ... ```. We clean that.
            clean_json = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)

            # 3. Construct the Plan
            return AnalysisPlan(
                original_query=query,
                source=data["source"],
                topic=data["topic"],
                target_country=data["target_country"],
                target_indicator=data["target_indicator"],
                years=[2018, 2019, 2020, 2021, 2022]
            )

        except Exception as e:
            print(f"[Planner Error] {e}")
            # Fallback logic could go here, but for now we raise
            raise ValueError(f"Could not plan query. AI Error: {e}")