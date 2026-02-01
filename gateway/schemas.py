from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """
    What the user sends us.
    Example: {"text": "Show me GDP growth in India vs China"}
    """
    text: str = Field(..., min_length=5, max_length=300, description="The analysis question")

class QueryResponse(BaseModel):
    """
    What we send back (initially).
    """
    query_id: str
    status: str
    result: dict | None = None