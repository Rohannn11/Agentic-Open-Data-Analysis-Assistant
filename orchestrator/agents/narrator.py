import os
import google.generativeai as genai
from dotenv import load_dotenv

from orchestrator.logger import get_logger

load_dotenv()
logger = get_logger("NarratorAgent")

class NarratorAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
           logger.warning("GEMINI_API_KEY missing. Narrator disabled.")
           self.model = None
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')

    def summarize(self, country: list | str, indicator: list | str, stats: dict) -> str:
        """
        Generates a narrative. 
        - If multiple countries are detected, it runs a Comparative Analysis.
        - If a single country is detected, it runs YOUR detailed Deep-Dive prompt.
        """
        if not self.model:
            return "Narrator disabled."

        # 1. DETECT MODE (Single vs Multi)
        # We look at the data_sources to see how many unique countries we actually have data for.
        sources = stats.get('data_sources', [])
        unique_countries = set()
        for s in sources:
            # Extract code from "WORLDBANK: GDP (IND)" -> "IND"
            if "(" in s and ")" in s:
                code = s.split("(")[-1].replace(")", "")
                unique_countries.add(code)
        
        # Fallback if parsing fails
        if not unique_countries:
            # Use the input arguments if we can't parse sources
            if isinstance(country, list):
                unique_countries = set(country)
            else:
                unique_countries = {country}

        is_comparison = len(unique_countries) > 1
        
        # Get primary country name for the prompt
        primary_country = list(unique_countries)[0] if unique_countries else "the target region"
        logger.info(f"Generating narrative. Mode: {'COMPARISON' if is_comparison else 'DEEP_DIVE'}")
        # 2. SELECT PROMPT
        if is_comparison:
            # --- MODE A: COMPARATIVE (New Logic) ---
            print(f"[Narrator] Detected Comparison between {unique_countries}")
            prompt = f"""
            You are a Senior Economic Analyst.
            
            TASK: Write a comparative analysis report.
            
            DATASETS:
            {stats.get('data_sources')}
            
            HEADLINE STATS (Aggregated):
            - Trend Direction: {stats.get('trend_direction')}
            - Average: {stats.get('average')}
            - Growth: {stats.get('growth_rate')}%

            INSTRUCTIONS:
            1. Compare the performance of the countries listed in the datasets.
            2. Highlight who is leading and who is lagging.
            3. Explain any diverging trends clearly.
            4. Strictly cite the data sources.
            5. Use Markdown (### Headers, **Bold**).
            """
        
        else:
            # --- MODE B: DEEP DIVE (Your Specific Prompt) ---
            print(f"[Narrator] Detected Single Country Deep-Dive for {primary_country}")
            
            # We use YOUR exact template here
            prompt = f"""
            You are an expert economic analyst. 
            Write a detailed report in proper points on {primary_country} regarding the requested indicators.

            SECTION 1: HARD FACTS (Strictly use ONLY these numbers)
            - Trend: {stats.get('trend_direction')}
            - Average: {stats.get('average')}
            - Growth: {stats.get('growth_rate')}%
            - Volatility: Low of {stats.get('min_value')} to High of {stats.get('max_value')}

            SECTION 2: CONTEXT (Use your own knowledge)
            - Briefly explain WHY this indicator matters for {primary_country} and what are the factors influencing it.
            - Explain general information about the demographics of {primary_country}.
            - Discuss any known economic events or policies in {primary_country} that could have impacted this indicator.
            - Provide a professional analysis of what this trend means for the future outlook of {primary_country}.
            - Do NOT invent specific numbers for this section, just qualitative context.

            OUTPUT FORMAT:
            Combine the facts and context into a smooth, professional paragraph and bullet points. Use Markdown formatting (###, **, -).
            """

        # 3. GENERATE
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Narrator failed: {e}")
            return f"Error generation narrative: {str(e)}"