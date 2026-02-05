import statistics
from typing import List
from data.canonical import IndicatorSeries
from orchestrator.schemas import AnalysisResult, ChartData, ChartDataset

class AnalystAgent:
    def analyze(self, data_list: List[IndicatorSeries]) -> AnalysisResult:
        
        if not data_list:
            return AnalysisResult(
                min_value=0, max_value=0, average=0, trend_direction="no_data", 
                growth_rate=0, chart_data=None, data_sources=[]
            )

        # 1. Prepare Visualization (Multi-Line)
        datasets = []
        all_sources = []
        
        # Dynamic Color Palette (Indigo, Emerald, Amber, Rose, Violet, Cyan)
        colors = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]
        
        for idx, series in enumerate(data_list):
            values = [pt.value for pt in series.data]
            if not values: continue
            
            # Create Citation (e.g., "WORLDBANK: GDP (IND)")
            all_sources.append(f"{series.source}: {series.indicator} ({series.country})")
            
            # Add Line to Chart
            datasets.append(ChartDataset(
                label=f"{series.country} - {series.indicator}",
                data=values,
                borderColor=colors[idx % len(colors)], # Cycle through colors
                fill=False
            ))

        # 2. Compute "Headline" Stats
        # (For the Top Bar, we use the PRIMARY dataset - usually the first one requested)
        primary_series = data_list[0]
        p_values = [pt.value for pt in primary_series.data]
        
        min_val = min(p_values) if p_values else 0
        max_val = max(p_values) if p_values else 0
        avg_val = statistics.mean(p_values) if p_values else 0
        
        # Simple Trend Logic
        trend = "stable"
        if p_values:
            if p_values[-1] > p_values[0]: trend = "increasing"
            elif p_values[-1] < p_values[0]: trend = "decreasing"
            
        growth = 0.0
        if p_values and p_values[0] != 0:
            growth = ((p_values[-1] - p_values[0]) / abs(p_values[0])) * 100

        # 3. Final Packaging
        # We assume the Years are consistent across datasets for simplicity in this MVP
        years = [str(pt.year) for pt in primary_series.data] if primary_series.data else []

        chart = ChartData(labels=years, datasets=datasets)

        return AnalysisResult(
            min_value=round(min_val, 2),
            max_value=round(max_val, 2),
            average=round(avg_val, 2),
            trend_direction=trend,
            growth_rate=round(growth, 2),
            chart_data=chart,
            data_sources=all_sources # <--- Full List of Sources
        )