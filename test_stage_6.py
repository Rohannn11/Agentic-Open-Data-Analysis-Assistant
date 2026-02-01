from data.adapters.worldbank_adapter import WorldBankAdapter

print("--- TESTING STAGE 6: WORLD BANK ADAPTER ---")

try:
    # Initialize
    adapter = WorldBankAdapter()
    
    # Run a real query: GDP (NY.GDP.MKTP.KD.ZG) for India (IND)
    print("Fetching India GDP from World Bank API...")
    result = adapter.fetch_data("IND", "NY.GDP.MKTP.KD.ZG", 2018, 2022)
    
    # Validate the output is OUR format
    print("\n✅ SUCCESS! Received Canonical Data:")
    print(f"Source: {result.source}")
    print(f"Country: {result.country}")
    print(f"Data Points Found: {len(result.data)}")
    
    # Print the first few points
    for point in result.data:
        print(f"  - Year: {point.year} | Value: {point.value}%")

except Exception as e:
    print(f"\n❌ FAILED: {e}")