from typing import List, Literal

# Type alias for our supported sources (keeps things safe)
DataSource = Literal["WORLDBANK", "OECD"]

class DatasetRouterAgent:
    def __init__(self):
        # RULE ENGINE: Simple keyword mapping
        # In a real startup, this might be a database table.
        self.rules = {
            "gdp": "WORLDBANK",
            "inflation": "WORLDBANK",
            "trade": "WORLDBANK",
            "unemployment": "OECD",
            "earnings": "OECD",
            "labour": "OECD" # 'labour' or 'labor'
        }

    def determine_source(self, query: str) -> List[DataSource]:
        """
        Scans the query string for keywords and returns the best data source.
        Default fallback is WORLDBANK if unsure.
        """
        query_lower = query.lower()
        
        # 1. Check for OECD keywords
        # We check OECD specific terms first
        for keyword in ["unemployment", "earnings", "labour", "oecd"]:
            if keyword in query_lower:
                return ["OECD"]
        
        # 2. Check for World Bank keywords
        for keyword in ["gdp", "inflation", "trade", "population"]:
            if keyword in query_lower:
                return ["WORLDBANK"]
        
        # 3. Default Fallback
        # If we don't know, we default to World Bank (it has more general data)
        print(f"[Router] No keywords matched. Defaulting to WORLDBANK.")
        return ["WORLDBANK"]