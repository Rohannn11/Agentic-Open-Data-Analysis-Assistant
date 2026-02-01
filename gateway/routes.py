from fastapi import APIRouter, HTTPException
from gateway.schemas import QueryRequest, QueryResponse
import uuid

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def submit_query(request: QueryRequest):
    """
    Endpoint to receive analysis requests.
    """
    # 1. Generate a unique ID for this request (Traceability)
    query_id = str(uuid.uuid4())
    
    print(f"Received Request {query_id}: {request.text}")

    # 2. TODO: Forward to Orchestrator (Stage 3)
    # For now, we just acknowledge receipt.
    return QueryResponse(
        query_id=query_id,
        status="processing",
        result={"message": "Gateway received your query. Orchestrator is offline (Stage 3 coming soon)."}
    )