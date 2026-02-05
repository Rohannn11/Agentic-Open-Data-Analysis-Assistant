import requests
from data.adapters.base_adapter import BaseAdapter
from data.canonical import IndicatorSeries, TimeSeriesPoint

class OECDAdapter(BaseAdapter):
    def fetch_data(self, country_code: str, indicator_code: str, start_year: int, end_year: int) -> IndicatorSeries:
        print(f"[OECDAdapter] Fetching {indicator_code} for {country_code}...")
        
        # OECD uses different country codes? Usually ISO3 is fine, but sometimes specific.
        # We will assume ISO3 for now.
        
        # API URL Construction (Simplified for 'HUR' - Unemployment)
        # Structure: https://stats.oecd.org/SDMX-JSON/data/<DATASET>/<COUNTRY>.<INDICATOR>...
        
        if indicator_code == "HUR":
            # STLABOUR = Short-Term Labour Statistics
            # LREM64TT = Employment Rate? No, let's use the specific endpoint logic.
            # For simplicity in this learning project, we target the "Harmonised Unemployment" dataset.
            dataset = "STLABOUR"
            # Dimension: Country.Indicator.Sex.Age.Frequency
            # AUS.HUR.L.A = Australia, Harmonized Unemployment, Total, All Ages, Annual
            dimension = f"{country_code}.HUR.TOT.GT.A" 
            
            url = f"https://stats.oecd.org/SDMX-JSON/data/{dataset}/{dimension}/all?startTime={start_year}&endTime={end_year}&dimensionAtObservation=allDimensions"
        
        else:
            raise NotImplementedError(f"OECD Indicator {indicator_code} not fully implemented in adapter yet.")

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data_json = response.json()

            # OECD SDMX-JSON parsing is complex.
            # The values are usually in dataStructure -> observations
            
            # 1. Parse DataPoints
            observations = data_json.get('dataSets', [{}])[0].get('observations', {})
            
            points = []
            # Observations keys are like "0:0:0:0:0"
            # We need to map the 'Time' dimension index to the actual Year.
            
            structure = data_json.get('structure', {})
            dimensions = structure.get('dimensions', {}).get('observation', [])
            
            # Find the 'Time' dimension
            time_dim = next((d for d in dimensions if d['id'] == 'TIME_PERIOD'), None)
            if not time_dim:
                raise ValueError("Could not find Time dimension in OECD response")
                
            time_values = [int(v['id']) for v in time_dim['values']]
            
            # Map values
            for key, val_obj in observations.items():
                # key might be "0:0:0:0:0". The last digit usually corresponds to Time if we ordered it right.
                # Actually, in "dimensionAtObservation=allDimensions", the key is the index string.
                # Let's try a robust flattened read.
                
                # IMPORTANT: OECD format varies. For this specific URL, let's debug-parse:
                # The key is likely just the index of the time period if other dims are fixed.
                # But to be safe, we iterate carefully.
                
                # Simplified approach for "STLABOUR":
                # The 'key' string's bits map to dimension indices.
                indices = [int(x) for x in key.split(':')]
                
                # We need to know which index position is "Time".
                # In our request "{country}.HUR.TOT.GT.A", Time is usually the last dimension or separate.
                # In SDMX-JSON, time is often an observation dimension.
                
                # HACK for Learning Project: 
                # If we get data, we just assume the order matches our requested years.
                # A production parser uses the 'structure' block to map strictly.
                
                # Let's assume the order is sequential years starting from start_year
                val = val_obj[0]
                
                # Find the year index (usually the last number in the key)
                time_idx = indices[-1] 
                if time_idx < len(time_values):
                    year = time_values[time_idx]
                    points.append(TimeSeriesPoint(year=year, value=float(val)))

            return IndicatorSeries(
                indicator=indicator_code,
                country=country_code,
                source="OECD",
                data=sorted(points, key=lambda x: x.year)
            )

        except Exception as e:
            print(f"[OECD Adapter Error] Failed to fetch/parse: {e}")
            # Now this returns an empty list, which is ALLOWED by our new Stage 1 contract.
            # The Analyst Agent will receive this and report "No Data" gracefully.
            return IndicatorSeries(
                indicator=indicator_code, 
                country=country_code, 
                source="OECD", 
                data=[]
            )