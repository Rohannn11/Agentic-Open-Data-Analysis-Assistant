import requests
from data.adapters.base_adapter import BaseAdapter
from data.canonical import IndicatorSeries, TimeSeriesPoint

class WorldBankAdapter(BaseAdapter):
    def fetch_data(self, country_code: str, indicator_code: str, start_year: int, end_year: int) -> IndicatorSeries:
        # 1. Construct the URL (World Bank specific logic)
        # Format: http://api.worldbank.org/v2/country/{country}/indicator/{ind}?format=json&date={start}:{end}
        url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
        params = {
            "format": "json",
            "date": f"{start_year}:{end_year}",
            "per_page": 100  # Ensure we get all years
        }
        
        print(f"[WorldBankAdapter] Fetching: {url} with params {params}")
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status() # Raise error if 404/500
            
            raw_data = response.json()
            
            # World Bank Quirks:
            # - If no data, it returns a metadata list only.
            # - Valid data is in index [1].
            if len(raw_data) < 2 or not raw_data[1]:
                 raise ValueError(f"No data found for {country_code} - {indicator_code}")
                 
            wb_records = raw_data[1]
            
            # 2. TRANSFORM (The Critical Step)
            # Convert their "messy" dict to our "clean" TimeSeriesPoint
            points = []
            for record in wb_records:
                val = record.get("value")
                year = record.get("date")
                
                # Only keep valid numbers
                if val is not None and year is not None:
                    points.append(TimeSeriesPoint(
                        year=int(year),
                        value=float(val)
                    ))
            
            # Sort by year (ascending)
            points.sort(key=lambda x: x.year)
            
            # 3. Return Canonical Object
            return IndicatorSeries(
                indicator=indicator_code,
                country=country_code,
                source="WORLDBANK",
                data=points
            )
            
        except Exception as e:
            print(f"[WorldBankAdapter] Error: {e}")
            raise e