from pydantic import BaseModel
from typing import List, Optional

# --- Keep existing Request/Response classes ---
class QueryRequest(BaseModel):
    # ... (keep as is) ...
    text: str

class QueryResponse(BaseModel):
    # ... (keep as is) ...
    query_id: str
    status: str
    result: dict | None = None

class AnalysisPlan(BaseModel):
    original_query: str
    source: str
    topic: str
    target_countries: List[str]   # e.g. ["IND", "CHN"]
    target_indicators: List[str]  # e.g. ["NY.GDP.MKTP.KD.ZG"]
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
    min_value: float
    max_value: float
    average: float
    trend_direction: str
    growth_rate: float
    chart_data: Optional[ChartData] = None
    data_sources: List[str] # Essential for the Narrator to know what it's looking at