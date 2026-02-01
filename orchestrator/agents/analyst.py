from data.canonical import IndicatorSeries
from orchestrator.schemas import AnalysisResult
import statistics

class AnalystAgent:
    def analyze(self, data: IndicatorSeries) -> AnalysisResult:
        """
        Performs statistical analysis on the series.
        """
        print(f"[Analyst] Computing stats for {data.country}...")
        
        values = [pt.value for pt in data.data]
        
        if not values:
             # Handle empty data case safely
             return AnalysisResult(
                 min_value=0, max_value=0, average=0, 
                 trend_direction="no_data", growth_rate=0
             )

        # 1. Basic Stats
        min_val = min(values)
        max_val = max(values)
        avg_val = statistics.mean(values)
        
        # 2. Determine Trend (Simple approach)
        start_val = values[0]
        end_val = values[-1]
        
        if end_val > start_val * 1.05: # > 5% growth
            trend = "increasing"
        elif end_val < start_val * 0.95: # > 5% decline
            trend = "decreasing"
        else:
            trend = "stable"
            
        # 3. Calculate Growth Rate (Simple percentage change)
        # Avoid division by zero
        if start_val == 0:
            growth = 0.0
        else:
            growth = ((end_val - start_val) / abs(start_val)) * 100

        return AnalysisResult(
            min_value=round(min_val, 2),
            max_value=round(max_val, 2),
            average=round(avg_val, 2),
            trend_direction=trend,
            growth_rate=round(growth, 2)
        )