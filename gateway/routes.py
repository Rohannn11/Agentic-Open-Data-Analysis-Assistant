from fastapi import APIRouter, HTTPException
from gateway.schemas import QueryRequest, QueryResponse
from orchestrator.main import AgentOrchestrator # <--- IMPORT THE BRAIN
import uuid

router = APIRouter()

# Initialize the brain once (Singleton pattern)
orchestrator = AgentOrchestrator()

@router.post("/query", response_model=QueryResponse)
async def submit_query(request: QueryRequest):
    """
    Endpoint to receive analysis requests.
    """
    query_id = str(uuid.uuid4())
    print(f"Received Request {query_id}: {request.text}")

    # --- REAL INTEGRATION ---
    try:
        # Pass the text to the brain
        result = orchestrator.run_pipeline(request.text)
        
        return QueryResponse(
            query_id=query_id,
            status="success",
            result=result
        )
    except Exception as e:
        print(f"Error: {e}")
        return QueryResponse(
            query_id=query_id,
            status="error",
            result={"error": str(e)}
        )