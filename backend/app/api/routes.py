from fastapi import APIRouter, HTTPException
from app.agents.commerce_graph import run_commerce_agent
from app.models.schemas import SearchRequest, SearchResponse

router = APIRouter(prefix="/api", tags=["commerce"])

@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "CommercePilot"}

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    try:
        return await run_commerce_agent(request.query, request.session_id, request.history)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="CommercePilot could not process the request") from exc
