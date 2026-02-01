from pydantic import BaseModel
from typing import List, Optional

class AnalysisPlan(BaseModel):
    """
    The blueprint for the analysis. 
    The Planner must produce this object.
    """
    original_query: str
    source: str                 # "WORLDBANK" or "OECD"
    topic: str                  # e.g., "gdp", "unemployment"
    target_country: str         # ISO code: "IND", "USA", "FRA"
    target_indicator: str       # API Code: "NY.GDP.MKTP.KD.ZG"
    years: List[int]            # [2022, 2023]
    operation: str = "trend"    # "trend" or "correlation" (future proofing)