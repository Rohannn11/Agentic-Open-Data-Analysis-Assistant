from fastapi import FastAPI
from gateway.routes import router

# 1. Initialize the App
app = FastAPI(
    title="Agentic Open Data Analyst",
    description="API Gateway for the Multi-Agent Data Analysis System",
    version="1.0.0"
)

# 2. Include our routes
app.include_router(router, prefix="/api/v1")

# 3. Root endpoint (Health Check)
@app.get("/")
def health_check():
    return {"status": "online", "system": "Agentic Analyst Gateway"}