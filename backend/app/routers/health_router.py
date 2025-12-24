"""
Health check router.

This module provides endpoints for monitoring the health and status of the API.
"""

from datetime import datetime

from fastapi import APIRouter

from app.utils.validation import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Service status and timestamp
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )
