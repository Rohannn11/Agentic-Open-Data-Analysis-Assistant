import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class NarratorAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("⚠️ WARNING: GEMINI_API_KEY not found in .env. Narrator will be disabled.")
            self.model = None
        else:
            # Configure the Gemini API
            genai.configure(api_key=self.api_key)
            # 'gemini-1.5-flash' is the best balance of speed/quality for this
            self.model = genai.GenerativeModel('gemini-flash-latest')

    def summarize(self, country: str, indicator: str, stats: dict) -> str:
        if not self.model:
            return "Narrator disabled (No API Key)."

        # --- HYBRID PROMPT DESIGN ---
        prompt = f"""
        You are an expert economic analyst. 
        Write a brief report (3-4 sentences) on {country} regarding {indicator}.

        SECTION 1: HARD FACTS (Strictly use ONLY these numbers)
        - Trend: {stats.get('trend_direction')}
        - Average: {stats.get('average')}
        - Growth: {stats.get('growth_rate')}%
        - Volatility: Low of {stats.get('min_value')} to High of {stats.get('max_value')}

        SECTION 2: CONTEXT (Use your own knowledge)
        - Briefly explain WHY this indicator matters for {country} and what are the factors influencing it.
        - Explain general information about the demographics of {country}.
        - Do NOT invent specific numbers for this section, just qualitative context.

        OUTPUT FORMAT:
        Combine the facts and context into a smooth, professional paragraph. Do not use headers or bullet points in the final output.
        """

        try:
            print(f"[Narrator] Calling Gemini 1.5 Flash...")
            
            # Gemini call
            response = self.model.generate_content(prompt)
            
            return response.text.strip()
            
        except Exception as e:
            return f"Error from Gemini: {str(e)}"