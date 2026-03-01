"""
Health — GET /health endpoint.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from src.data.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health status."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.now(timezone.utc),
    )
