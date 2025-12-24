"""
Text-to-speech router.

This module provides endpoints for converting text to speech.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import io

from app.services.tts_service import get_tts_service
from app.utils.exceptions import AIServiceException
from app.utils.logging import get_logger
from app.utils.validation import TTSRequest, TTSResponse

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["tts"])


@router.post("/tts", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest):
    logger.debug(f"Received request for TTS with model: {request.model}")
    """
    Convert text to speech.
    
    Args:
        request: TTSRequest with text and optional parameters
        
    Returns:
        WAV audio file as binary data
        
    Raises:
        HTTPException: If synthesis fails
    """
    try:
        service = get_tts_service()
        
        audio_bytes, sample_rate = service.synthesize(
            text=request.text,
            model=request.model,
            speaker_id=request.speaker_id,
            speed=request.speed,
        )
        
        # Return audio as streaming response
        logger.debug(f"Successfully synthesized speech with model: {request.model}")
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=speech.wav"}
        )
    
    except AIServiceException as e:
        logger.error(f"TTS error: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except Exception as e:
        logger.error(f"Unexpected error in TTS: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
