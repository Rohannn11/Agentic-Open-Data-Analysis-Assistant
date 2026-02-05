from pydantic import BaseModel, field_validator
from typing import List, Literal

# 1. ENUMS / CONSTANTS
# We lock our naming conventions here. We don't want someone typing
# "gdp" in one place and "GDP" in another.
VALID_SOURCES = Literal["WORLDBANK", "OECD"]

class TimeSeriesPoint(BaseModel):
    """
    Represents a single data point in time.
    We strictly enforce yearly granularity (int) and float values.
    """
    year: int
    value: float

class IndicatorSeries(BaseModel):
    """
    The Master Data Object.
    Once data enters our system, it MUST look like this.
    """
    indicator: str   # e.g., "UNEMPLOYMENT_RATE"
    country: str     # e.g., "USA", "IND" (ISO 3-letter codes preferred)
    source: str      # e.g., "WORLDBANK" or "OECD"
    data: List[TimeSeriesPoint]

    # # OPTIONAL LEARNING: Validation logic
    # # This ensures we never get an empty dataset silently.
    # @field_validator('data')
    # def data_must_not_be_empty(cls, v):
    #     if not v:
    #         raise ValueError('IndicatorSeries must contain at least one data point')
    #     return v