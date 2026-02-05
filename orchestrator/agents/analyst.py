import statistics
from data.canonical import IndicatorSeries
from orchestrator.schemas import AnalysisResult, ChartData, ChartDataset

class AnalystAgent:
    def analyze(self, data: IndicatorSeries) -> AnalysisResult:
        """
        Performs stats AND formats data for Chart.js
        """
        print(f"[Analyst] Processing {len(data.data)} points for {data.country}...")
        
        # 1. Extract values
        values = [pt.value for pt in data.data]
        years = [str(pt.year) for pt in data.data] # Chart labels must be strings
        
        # 2. Handle Empty Data (Robustness check we added earlier)
        if not values:
            return AnalysisResult(
                min_value=0.0, max_value=0.0, average=0.0,
                trend_direction="no_data", growth_rate=0.0,
                chart_data=None
            )

        # 3. Calculate Stats
        min_val = min(values)
        max_val = max(values)
        avg_val = statistics.mean(values)
        
        start_val = values[0]
        end_val = values[-1]
        
        # Simple trend logic
        if end_val > start_val * 1.05:
            trend = "increasing"
        elif end_val < start_val * 0.95:
            trend = "decreasing"
        else:
            trend = "stable"
            
        growth = 0.0
        if start_val != 0:
            growth = ((end_val - start_val) / abs(start_val)) * 100

        # 4. PREPARE CHART PAYLOAD (The New Part)
        # We format strictly for the Frontend's expectation
        chart = ChartData(
            labels=years,
            datasets=[
                ChartDataset(
                    label=f"{data.indicator} ({data.country})",
                    data=values,
                    borderColor="#4F46E5", # Professional Indigo
                    fill=False
                )
            ]
        )

        return AnalysisResult(
            min_value=round(min_val, 2),
            max_value=round(max_val, 2),
            average=round(avg_val, 2),
            trend_direction=trend,
            growth_rate=round(growth, 2),
            chart_data=chart # <--- Attached!
        )