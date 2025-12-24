"""
Large Language Model router.

This module provides endpoints for text generation and conversation.
"""

from fastapi import APIRouter, HTTPException

from app.services.llm_service import get_llm_service
from app.utils.exceptions import AIServiceException
from app.utils.logging import get_logger
from app.utils.validation import LLMRequest, LLMResponse

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["llm"])


@router.post("/llm", response_model=LLMResponse)
async def generate_text(request: LLMRequest) -> LLMResponse:
    logger.debug(f"Received request to generate text for model: {request.model}")
    """
    Generate text based on conversation messages.
    
    Args:
        request: LLMRequest with messages and optional parameters
        
    Returns:
        LLMResponse with generated text and metadata
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        service = get_llm_service()
        
        result = service.generate(
            messages=request.messages,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
        )
        
        return LLMResponse(
            response=result["response"],
            model=result["model"],
            tokens_used=result.get("tokens_used"),
            stop_reason=result.get("stop_reason"),
        )
        logger.debug(f"Successfully generated text for model: {request.model}")
    
    except AIServiceException as e:
        logger.error(f"LLM error: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except Exception as e:
        logger.error(f"Unexpected error in LLM: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
