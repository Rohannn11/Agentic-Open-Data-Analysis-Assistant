import statistics
from typing import List
from data.canonical import IndicatorSeries
from orchestrator.schemas import AnalysisResult, ChartData, ChartDataset

class AnalystAgent:
    def analyze(self, data_list: List[IndicatorSeries]) -> AnalysisResult:
        if not data_list:
            return AnalysisResult(
                min_value=0, max_value=0, average=0, trend_direction="no_data", 
                growth_rate=0, chart_data=None, summary_chart_data=None, data_sources=[]
            )

        CODE_MAP = {
            "NY.GDP.MKTP.KD.ZG": "GDP Growth (%)",
            "FP.CPI.TOTL.ZG": "Inflation (%)",
            "SP.POP.TOTL": "Population",
            "HUR": "Unemployment (%)"
        }

        # 1. Prepare Line Chart (Trends)
        line_datasets = []
        bar_datasets = [] # New: For the comparison chart
        all_sources = []
        colors = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]
        
        # We need to collect averages for the bar chart
        bar_labels = [] 
        bar_values = []
        bar_colors = []

        for idx, series in enumerate(data_list):
            values = [pt.value for pt in series.data]
            if not values: continue
            
            metric_name = CODE_MAP.get(series.indicator, series.indicator)
            label = f"{series.country} - {metric_name}"
            all_sources.append(f"{series.source}: {metric_name} ({series.country})")
            
            # A. Add to Line Chart
            line_datasets.append(ChartDataset(
                label=label,
                data=values,
                borderColor=colors[idx % len(colors)],
                fill=False
            ))

            # B. Prepare Bar Chart Data (Average Performance)
            avg_val = statistics.mean(values)
            bar_labels.append(series.country) # Label x-axis with Country
            bar_values.append(avg_val)
            bar_colors.append(colors[idx % len(colors)])

        # 2. Stats (Primary)
        primary_series = data_list[0]
        p_values = [pt.value for pt in primary_series.data]
        
        min_val = min(p_values) if p_values else 0
        max_val = max(p_values) if p_values else 0
        avg_val = statistics.mean(p_values) if p_values else 0
        
        trend = "stable"
        if p_values:
            if p_values[-1] > p_values[0]: trend = "increasing"
            elif p_values[-1] < p_values[0]: trend = "decreasing"
            
        growth = 0.0
        if p_values:
             growth = p_values[-1] - p_values[0] # Using Points difference for Rates

        years = [str(pt.year) for pt in primary_series.data] if primary_series.data else []

        # 3. Package BOTH Charts
        line_chart = ChartData(labels=years, datasets=line_datasets)
        
        # New: Summary Bar Chart
        # We package it slightly differently: One dataset, multiple colored bars
        summary_chart = ChartData(
            labels=[d.label for d in line_datasets], # Use full labels "IND - GDP"
            datasets=[
                ChartDataset(
                    label="Average Value",
                    data=bar_values,
                    borderColor="#ffffff",
                    fill=True # Bars are filled
                )
            ]
        )
        # Note: We will handle the custom bar colors in the frontend for simplicity, 
        # or we could pass them here. For now, let's keep the contract simple.

        return AnalysisResult(
            min_value=round(min_val, 2),
            max_value=round(max_val, 2),
            average=round(avg_val, 2),
            trend_direction=trend,
            growth_rate=round(growth, 2),
            chart_data=line_chart,          # Chart 1
            summary_chart_data=summary_chart, # Chart 2 <--- NEW
            data_sources=all_sources
        )