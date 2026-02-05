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
    # ... (keep as is) ...
    original_query: str
    source: str
    topic: str
    target_country: str
    target_indicator: str
    years: List[int]

# --- NEW VISUALIZATION SCHEMAS ---
class ChartDataset(BaseModel):
    label: str
    data: List[float]
    borderColor: str = "#4F46E5"
    fill: bool = False

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[ChartDataset]

# --- UPDATE ANALYSIS RESULT ---
class AnalysisResult(BaseModel):
    min_value: float
    max_value: float
    average: float
    trend_direction: str
    growth_rate: float
    # New Field (Optional, because sometimes there is no data)
    chart_data: Optional[ChartData] = None