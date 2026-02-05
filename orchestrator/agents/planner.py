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
            raise ValueError("GEMINI_API_KEY required for Planner")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def create_plan(self, query: str) -> AnalysisPlan:
        print(f"[Planner] Designing plan for: '{query}'")

        prompt = f"""
        You are an Expert Data Planner.
        
        USER QUERY: "{query}"

        AVAILABLE METRICS (Use these exact codes):
        1. WORLDBANK:
           - GDP Growth: "NY.GDP.MKTP.KD.ZG"
           - Inflation: "FP.CPI.TOTL.ZG"
           - Population: "SP.POP.TOTL"
        2. OECD:
           - Unemployment Rate: "HUR"

        INSTRUCTIONS:
        1. **Extract Countries**: Identify ALL countries mentioned. Convert to ISO 3-letter codes (e.g., "India and China" -> ["IND", "CHN"]). 
           - If NO country is mentioned, default to ["USA"].
        2. **Determine Indicator**: Pick the single most relevant indicator code.
        3. **Context Rule**: 
           - If the query is about GDP, ALWAYS add Inflation ("FP.CPI.TOTL.ZG") to the list for context.
           - If the query is about Unemployment, ALWAYS add Inflation ("FP.CPI.TOTL.ZG").
        4. **Select Source**: Choose WORLDBANK or OECD based on the primary indicator.

        RETURN JSON ONLY:
        {{
            "target_countries": ["ISO1", "ISO2"],
            "target_indicators": ["PRIMARY_CODE", "CONTEXT_CODE"],
            "source": "WORLDBANK", 
            "topic": "economic_analysis"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            clean_json = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(clean_json)

            return AnalysisPlan(
                original_query=query,
                source=data["source"],
                topic=data["topic"],
                target_countries=data["target_countries"],
                target_indicators=data["target_indicators"],
                years=[2018, 2019, 2020, 2021, 2022]
            )

        except Exception as e:
            print(f"[Planner Error] {e}")
            # Fallback
            return AnalysisPlan(
                original_query=query, source="WORLDBANK", topic="error_fallback",
                target_countries=["USA"], target_indicators=["NY.GDP.MKTP.KD.ZG"], 
                years=[2020, 2021, 2022]
            )