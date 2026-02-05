from pydantic import BaseModel, Field
from pydantic import BaseModel
from typing import List, Optional
class QueryRequest(BaseModel):
    """
    What the user sends us.
    Example: {"text": "Show me GDP growth in India vs China"}
    """
    text: str = Field(..., min_length=5, max_length=300, description="The analysis question")

class QueryResponse(BaseModel):
    """
    What we send back (initially).
    """
    query_id: str
    status: str
    result: dict | None = None
    
class AnalysisPlan(BaseModel):
    original_query: str
    source: str
    topic: str
    # CHANGE 1: Plural Countries
    target_countries: List[str]   # e.g., ["IND", "CHN", "BRA"]
    # CHANGE 2: Contextual Indicators
    target_indicators: List[str]  # e.g., ["NY.GDP.MKTP.KD.ZG", "SP.POP.TOTL"]
    years: List[int]

class ChartDataset(BaseModel):
    label: str
    data: List[float]
    borderColor: str
    fill: bool = False

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[ChartDataset]

class AnalysisResult(BaseModel):
    # We will aggregate stats per country, but for the summary, we keep these generic
    # or we could make them lists. For simplicity, let's keep specific metrics generic
    # but rely on the Chart and Narrative for the comparison details.
    
    chart_data: Optional[ChartData] = None
    # CHANGE 3: Explicit Citations
    data_sources: List[str] # e.g., ["World Bank: GDP", "World Bank: Population"]        