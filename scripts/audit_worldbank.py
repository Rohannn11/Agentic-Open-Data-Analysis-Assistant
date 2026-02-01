import requests
import json
import time

def audit_worldbank(country_iso="IND", indicator="NY.GDP.MKTP.CD"):
    """
    Fetches data to understand structure, pagination, and latency.
    """
    # format=json is critical, otherwise it defaults to XML
    url = f"http://api.worldbank.org/v2/country/{country_iso}/indicator/{indicator}"
    params = {
        "format": "json",
        "date": "2020:2022", # Limit range for testing
        "per_page": 100      # Max is usually higher, but good for control
    }

    print(f"📡 Requesting: {url}")
    start_time = time.time()
    response = requests.get(url, params=params)
    latency = time.time() - start_time
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        return

    data = response.json()
    
    # ANALYSIS OF STRUCTURE
    # World Bank returns a list of size 2.
    # index 0: Metadata (pagination info)
    # index 1: List of actual data points
    
    metadata = data[0]
    records = data[1]

    print(f"✅ Success! Latency: {latency:.4f}s")
    print(f"📄 Metadata (Pagination): {json.dumps(metadata, indent=2)}")
    print(f"📊 Sample Record (First item): {json.dumps(records[0], indent=2)}")

if __name__ == "__main__":
    audit_worldbank()

    