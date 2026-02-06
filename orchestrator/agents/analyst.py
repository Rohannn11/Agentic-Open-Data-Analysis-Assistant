import statistics
from typing import List
from data.canonical import IndicatorSeries
from orchestrator.schemas import AnalysisResult, ChartData, ChartDataset
from orchestrator.logger import get_logger

logger = get_logger("AnalystAgent")

class AnalystAgent:
    def analyze(self, data_list: List[IndicatorSeries]) -> AnalysisResult:
        logger.info(f"Analyzing {len(data_list)} datasets.")
        
        if not data_list:
            logger.warning("No datasets to analyze. Returning empty result.")
            return AnalysisResult(
                min_value=0, max_value=0, average=0, trend_direction="no_data", 
                growth_rate=0, chart_data=None, summary_chart_data=None, data_sources=[]
            )

        CODE_MAP = {
            "NY.GDP.MKTP.KD.ZG": "GDP Growth (%)",
            "FP.CPI.TOTL.ZG": "Inflation (%)",
            "SP.POP.TOTL": "Population",
            "EN.ATM.CO2E.KT": "CO2 Emissions",
            "HUR": "Unemployment (%)",
            "EARNINGS": "Hourly Earnings"
        }

        # 1. Prepare Line Chart
        line_datasets = []
        bar_values = []
        all_sources = []
        colors = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]
        
        for idx, series in enumerate(data_list):
            values = [pt.value for pt in series.data]
            if not values: continue
            
            metric_name = CODE_MAP.get(series.indicator, series.indicator)
            label = f"{series.country} - {metric_name}"
            all_sources.append(f"{series.source}: {metric_name} ({series.country})")
            
            # Line Chart Data
            line_datasets.append(ChartDataset(
                label=label,
                data=values,
                borderColor=colors[idx % len(colors)],
                fill=False
            ))

            # Bar Chart Data (Average)
            bar_values.append(statistics.mean(values))

        # 2. Stats (Primary)
        primary = data_list[0]
        p_vals = [pt.value for pt in primary.data]
        
        min_val = min(p_vals) if p_vals else 0
        max_val = max(p_vals) if p_vals else 0
        avg_val = statistics.mean(p_vals) if p_vals else 0
        
        trend = "stable"
        if p_vals:
            if p_vals[-1] > p_vals[0]: trend = "increasing"
            elif p_vals[-1] < p_vals[0]: trend = "decreasing"
            
        growth = 0.0
        if p_vals:
            is_rate = any(k in primary.indicator for k in ["ZG", "HUR", "CPI"])
            if is_rate:
                growth = p_vals[-1] - p_vals[0] # Point difference
            elif p_vals[0] != 0:
                growth = ((p_vals[-1] - p_vals[0]) / abs(p_vals[0])) * 100

        # 3. Packaging
        years = [str(pt.year) for pt in primary.data] if primary.data else []
        
        # Dual Charts
        line_chart = ChartData(labels=years, datasets=line_datasets)
        
        summary_chart = ChartData(
            labels=[d.label for d in line_datasets],
            datasets=[ChartDataset(label="Average", data=bar_values, borderColor="#fff", fill=True)]
        )

        return AnalysisResult(
            min_value=round(min_val, 2),
            max_value=round(max_val, 2),
            average=round(avg_val, 2),
            trend_direction=trend,
            growth_rate=round(growth, 2),
            chart_data=line_chart,
            summary_chart_data=summary_chart,
            data_sources=all_sources
        )