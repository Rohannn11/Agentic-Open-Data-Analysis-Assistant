from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- NEW IMPORT
from gateway.routes import router

app = FastAPI(
    title="Agentic Open Data Analyst",
    description="API Gateway for the Multi-Agent Data Analysis System",
    version="1.0.0"
)

# --- ENABLE CORS (Allow Frontend to talk to Backend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "online", "system": "Agentic Analyst Gateway"}