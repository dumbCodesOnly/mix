"""
Speech-to-text service.

This module handles converting speech to text using HuggingFace models.
"""

from typing import Optional

from app.services.hf_client import get_hf_client
from app.utils.config import Config
from app.utils.exceptions import HuggingFaceAPIError, ProcessingError
from app.utils.logging import get_logger

logger = get_logger(__name__)


class STTService:
    """Service for speech-to-text conversion."""
    
    def __init__(self):
        """Initialize the STT service."""
        self.hf_client = get_hf_client()
    
    def transcribe(
        self,
        audio_bytes: bytes,
        model: Optional[str] = None,
        language: Optional[str] = None,
    ) -> dict:
        """
        Convert speech to text.
        
        Args:
            audio_bytes: Audio data as bytes
            model: Model to use (uses default if None)
            language: Language code (e.g., 'en', 'fr')
            
        Returns:
            dict: Transcription result with 'text' and metadata
            
        Raises:
            HuggingFaceAPIError: If transcription fails
            ProcessingError: If audio processing fails
        """
        model = model or Config.DEFAULT_STT_MODEL
        
        try:
            logger.info(
                f"Transcribing audio with model {model}",
                extra={"audio_size": len(audio_bytes), "model": model, "language": language}
            )
            
            # Call HuggingFace API
            result = self.hf_client.automatic_speech_recognition(
                audio=audio_bytes,
                model=model,
            )
            
            # Ensure result is a dictionary
            if isinstance(result, str):
                result = {"text": result}
            
            # Add language if provided
            if language:
                result["language"] = language
            
            logger.info(
                f"Audio transcribed successfully",
                extra={"text_length": len(result.get("text", "")), "model": model}
            )
            
            return result
        
        except HuggingFaceAPIError:
            raise
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise ProcessingError(f"Failed to transcribe audio: {str(e)}", "stt")


# Global service instance
_stt_service: Optional[STTService] = None


def get_stt_service() -> STTService:
    """
    Get or create the global STT service instance.
    
    Returns:
        STTService: The global service instance
    """
    global _stt_service
    if _stt_service is None:
        _stt_service = STTService()
    return _stt_service
