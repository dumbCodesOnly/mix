"""
Text-to-speech service.

This module handles converting text to speech using HuggingFace models.
"""

from typing import Optional

from app.services.hf_client import get_hf_client
from app.utils.config import Config
from app.utils.exceptions import HuggingFaceAPIError, ProcessingError
from app.utils.logging import get_logger

logger = get_logger(__name__)


class TTSService:
    """Service for text-to-speech conversion."""
    
    def __init__(self):
        """Initialize the TTS service."""
        self.hf_client = get_hf_client()
    
    def synthesize(
        self,
        text: str,
        model: Optional[str] = None,
        speaker_id: int = 0,
        speed: float = 1.0,
    ) -> tuple[bytes, int]:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            model: Model to use (uses default if None)
            speaker_id: Speaker ID for multi-speaker models
            speed: Speech speed multiplier (0.5-2.0)
            
        Returns:
            tuple: (audio_bytes, sample_rate)
            
        Raises:
            HuggingFaceAPIError: If synthesis fails
            ProcessingError: If audio processing fails
        """
        model = model or Config.DEFAULT_TTS_MODEL
        
        try:
            logger.info(
                f"Synthesizing speech with model {model}",
                extra={"text_length": len(text), "model": model}
            )
            
            # Call HuggingFace API
            audio_bytes = self.hf_client.text_to_speech(
                text=text,
                model=model,
                speaker_id=speaker_id,
            )
            
            # Default sample rate for most TTS models
            sample_rate = 22050
            
            logger.info(
                f"Speech synthesized successfully",
                extra={"audio_size": len(audio_bytes), "sample_rate": sample_rate}
            )
            
            return audio_bytes, sample_rate
        
        except HuggingFaceAPIError:
            raise
        except Exception as e:
            logger.error(f"Error synthesizing speech: {str(e)}")
            raise ProcessingError(f"Failed to synthesize speech: {str(e)}", "tts")


# Global service instance
_tts_service: Optional[TTSService] = None


def get_tts_service() -> TTSService:
    """
    Get or create the global TTS service instance.
    
    Returns:
        TTSService: The global service instance
    """
    global _tts_service
    if _tts_service is None:
        _tts_service = TTSService()
    return _tts_service
