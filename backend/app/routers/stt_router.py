"""
Speech-to-text router.

This module provides endpoints for converting speech to text.
"""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from app.services.stt_service import get_stt_service
from app.utils.exceptions import AIServiceException, FileSizeError
from app.utils.logging import get_logger
from app.utils.config import Config

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["stt"])


class STTResponse(BaseModel):
    """Response model for speech-to-text."""
    text: str
    language: str | None = None
    confidence: float | None = None
    model: str


@router.post("/stt", response_model=STTResponse)
async def speech_to_text(
    logger.debug(f"Received request for STT with model: {model}")
    audio: UploadFile = File(...),
    model: str | None = Form(None),
    language: str | None = Form(None),
):
    """
    Convert speech to text.
    
    Args:
        audio: Audio file (WAV, MP3, etc.)
        model: Model to use (optional)
        language: Language code (optional)
        
    Returns:
        STTResponse with transcribed text and metadata
        
    Raises:
        HTTPException: If transcription fails
    """
    try:
        # Read audio file
        audio_bytes = await audio.read()
        
        # Check file size
        if len(audio_bytes) > Config.MAX_AUDIO_SIZE:
            raise FileSizeError(
                len(audio_bytes),
                Config.MAX_AUDIO_SIZE,
                "audio"
            )
        
        service = get_stt_service()
        
        result = service.transcribe(
            audio_bytes=audio_bytes,
            model=model,
            language=language,
        )
        
        return STTResponse(
            text=result.get("text", ""),
            language=result.get("language", language),
            confidence=result.get("confidence"),
            model=result.get("model", model or Config.DEFAULT_STT_MODEL),
        )
        logger.debug(f"Successfully transcribed audio with model: {model}")
    
    except AIServiceException as e:
        logger.error(f"STT error: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except Exception as e:
        logger.error(f"Unexpected error in STT: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
