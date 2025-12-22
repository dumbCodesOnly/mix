"""
Embeddings router.

This module provides endpoints for generating text embeddings.
"""

from fastapi import APIRouter, HTTPException

from app.services.embedding_service import get_embedding_service
from app.utils.exceptions import AIServiceException
from app.utils.logging import get_logger
from app.utils.validation import EmbeddingRequest, EmbeddingResponse

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["embedding"])


@router.post("/embedding", response_model=EmbeddingResponse)
async def generate_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Generate embeddings for text.
    
    Args:
        request: EmbeddingRequest with text and optional model
        
    Returns:
        EmbeddingResponse with embedding vector and metadata
        
    Raises:
        HTTPException: If embedding generation fails
    """
    try:
        service = get_embedding_service()
        
        result = service.embed(
            text=request.text,
            model=request.model,
        )
        
        return EmbeddingResponse(
            embedding=result["embedding"],
            dimension=result["dimension"],
            model=result["model"],
            tokens_used=result.get("tokens_used"),
        )
    
    except AIServiceException as e:
        logger.error(f"Embedding error: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except Exception as e:
        logger.error(f"Unexpected error in embedding: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
