"""
HuggingFace Inference API client wrapper.

This module provides a centralized interface to the HuggingFace Inference API,
with support for retry logic, model fallback, and comprehensive error handling.
"""

# The InferenceClient handles model routing automatically.
# Overriding the endpoint can cause non-LLM tasks to fail.
import os

from typing import Any, Optional

from huggingface_hub import InferenceClient

from app.utils.config import Config
from app.utils.exceptions import HuggingFaceAPIError, ModelNotFoundError, TimeoutError
from app.utils.logging import get_logger
from app.utils.retry import retry

# Mapping of models that require a specific provider
# Based on HuggingFace Inference API documentation for specific models
MODEL_PROVIDER_MAP = {
    # Video Models (Require 'novita' provider)
    "Wan-AI/Wan2.1-T2V-14B": "novita",
    "Wan-AI/Wan2.2-TI2V-5B": "novita",
    "Wan-AI/Wan2.2-T2V-A14B": "novita",
    "tencent/HunyuanVideo-1.5": "novita",
    "meituan-longcat/LongCat-Video": "novita", # Based on similar model type and provider pattern

    # TTS Models (Require 'fal' provider)
    "hexgrad/Kokoro-82M": "fal",
    "microsoft/VibeVoice-Realtime-0.5B": "fal", # Based on similar model type and provider pattern
    "ResembleAI/chatterbox": "fal", # Based on similar model type and provider pattern

    # Image Models (Require 'fal' provider)
    "black-forest-labs/FLUX.1-dev": "fal",
}

def get_provider_for_model(model: str) -> Optional[str]:
    """Returns the required provider for a given model, or None if not required."""
    return MODEL_PROVIDER_MAP.get(model)

logger = get_logger(__name__)


class HuggingFaceClient:
    """
    Wrapper around HuggingFace InferenceClient with enhanced error handling.
    
    This class provides a single interface for all HuggingFace API calls,
    with automatic retry logic, timeout handling, and model fallback support.
    """
    
    def __init__(self, api_key: str = Config.HF_API_KEY):
        """
        Initialize the HuggingFace client.
        
        Args:
            api_key: HuggingFace API key
            
        Raises:
            ValueError: If API key is not provided
        """
        if not api_key:
            raise ValueError("HuggingFace API key is required")
        
        self.api_key = api_key
        self.client = InferenceClient(token=api_key)
        logger.info(f"HuggingFace client initialized with endpoint: {os.environ.get('HF_INFERENCE_ENDPOINT')}")
    
    @retry()
    def text_to_image(
        self,
        prompt: str,
        model: str = Config.DEFAULT_IMAGE_MODEL,
        negative_prompt: Optional[str] = None,
        height: int = 512,
        width: int = 512,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
    ) -> bytes:
        """
        logger.debug(f"Entering text_to_image with model: {model}")
        Generate an image from a text prompt.
        
        Args:
            prompt: Text description of the image to generate
            model: Model to use for generation
            negative_prompt: Text to exclude from generation
            height: Image height in pixels
            width: Image width in pixels
            num_inference_steps: Number of inference steps
            guidance_scale: Guidance scale for prompt adherence
            
        Returns:
            bytes: Generated image as PNG binary data
            
        Raises:
            HuggingFaceAPIError: If the API call fails
            TimeoutError: If the request times out
        """
        try:
            logger.info(
                f"Generating image with model {model}",
                extra={"prompt": prompt[:100], "model": model}
            )
            
            image = self.client.text_to_image(
                prompt=prompt,
                model=model,
                negative_prompt=negative_prompt,
                height=height,
                width=width,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                provider=get_provider_for_model(model),
            )
            
            # Convert PIL Image to bytes
            import io
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            
            logger.debug(f"Exiting text_to_image successfully with model {model}")
            return image_bytes.getvalue()
        
        except TimeoutError as e:
            logger.error(f"Timeout generating image with model {model}: {str(e)}")
            raise TimeoutError(f"Image generation timed out: {str(e)}", Config.REQUEST_TIMEOUT)
        
        except Exception as e:
            logger.error(f"Error generating image with model {model}: {str(e)}")
            raise HuggingFaceAPIError(f"Failed to generate image: {str(e)}")
    
    @retry()
    def image_to_image(
        self,
        image: Any,
        prompt: str,
        model: str = Config.DEFAULT_IMAGE_MODEL,
        negative_prompt: Optional[str] = None,
        strength: float = 0.75,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
    ) -> bytes:
        """
        logger.debug(f"Entering image_to_image with model: {model}")
        Transform an image based on a text prompt.
        
        Args:
            image: PIL Image or image bytes to transform
            prompt: Text description for the transformation
            model: Model to use for transformation
            negative_prompt: Text to exclude from generation
            strength: Strength of the transformation (0-1)
            num_inference_steps: Number of inference steps
            guidance_scale: Guidance scale for prompt adherence
            
        Returns:
            bytes: Transformed image as PNG binary data
            
        Raises:
            HuggingFaceAPIError: If the API call fails
            TimeoutError: If the request times out
        """
        try:
            logger.info(
                f"Transforming image with model {model}",
                extra={"prompt": prompt[:100], "model": model}
            )
            
            result = self.client.image_to_image(
                image=image,
                prompt=prompt,
                model=model,
                negative_prompt=negative_prompt,
                strength=strength,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                provider=get_provider_for_model(model),
            )
            
            # Convert PIL Image to bytes
            import io
            image_bytes = io.BytesIO()
            result.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            
            logger.debug(f"Exiting image_to_image successfully with model {model}")
            return image_bytes.getvalue()
        
        except TimeoutError as e:
            logger.error(f"Timeout transforming image with model {model}: {str(e)}")
            raise TimeoutError(f"Image transformation timed out: {str(e)}", Config.REQUEST_TIMEOUT)
        
        except Exception as e:
            logger.error(f"Error transforming image with model {model}: {str(e)}")
            raise HuggingFaceAPIError(f"Failed to transform image: {str(e)}")
    
    @retry()
    def inpainting(
        self,
        image: Any,
        mask: Any,
        prompt: str,
         model: str = Config.DEFAULT_EMBEDDING_MODEL,
        negative_prompt: Optional[str] = None,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
    ) -> bytes:
        """
        logger.debug(f"Entering inpainting with model: {model}")
        Perform image inpainting (editing with mask).
        
        Args:
            image: PIL Image or image bytes to inpaint
            mask: PIL Image or mask bytes (white areas are inpainted)
            prompt: Text description for the inpainting
            model: Model to use for inpainting
            negative_prompt: Text to exclude from generation
            num_inference_steps: Number of inference steps
            guidance_scale: Guidance scale for prompt adherence
            
        Returns:
            bytes: Inpainted image as PNG binary data
            
        Raises:
            HuggingFaceAPIError: If the API call fails
            TimeoutError: If the request times out
        """
        try:
            logger.info(
                f"Inpainting image with model {model}",
                extra={"prompt": prompt[:100], "model": model}
            )
            
            result = self.client.inpainting(
                image=image,
                mask_image=mask,
                prompt=prompt,
                model=model,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                provider=get_provider_for_model(model),
            )
            
            # Convert PIL Image to bytes
            import io
            image_bytes = io.BytesIO()
            result.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            
            logger.debug(f"Exiting inpainting successfully with model {model}")
            return image_bytes.getvalue()
        
        except TimeoutError as e:
            logger.error(f"Timeout inpainting image with model {model}: {str(e)}")
            raise TimeoutError(f"Image inpainting timed out: {str(e)}", Config.REQUEST_TIMEOUT)
        
        except Exception as e:
            logger.error(f"Error inpainting image with model {model}: {str(e)}")
            raise HuggingFaceAPIError(f"Failed to inpaint image: {str(e)}")
    
    @retry()
    def text_to_speech(
        self,
        text: str,
        model: str = Config.DEFAULT_TTS_MODEL,
        speaker_id: int = 0,
    ) -> bytes:
        """
        logger.debug(f"Entering text_to_speech with model: {model}")
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            model: Model to use for TTS
            speaker_id: Speaker ID for multi-speaker models
            
        Returns:
            bytes: Generated audio as WAV binary data
            
        Raises:
            HuggingFaceAPIError: If the API call fails
            TimeoutError: If the request times out
        """
        try:
            logger.info(
                f"Converting text to speech with model {model}",
                extra={"text": text[:100], "model": model}
            )
            
            provider = get_provider_for_model(model)
            logger.info(
                f"Converting text to speech with model {model} (Provider: {provider})",
                extra={"text": text[:100], "model": model, "provider": provider}
            )
            audio = self.client.text_to_speech(
                text=text,
                model=model,
                provider=provider,
            )
            
            logger.debug(f"Exiting text_to_speech successfully with model {model}")
            return audio
        
        except TimeoutError as e:
            logger.error(f"Timeout converting text to speech with model {model}: {str(e)}")
            raise TimeoutError(f"Text-to-speech timed out: {str(e)}", Config.REQUEST_TIMEOUT)
        
        except Exception as e:
            logger.error(f"Error converting text to speech with model {model}: {str(e)}")
            raise HuggingFaceAPIError(f"Failed to convert text to speech: {str(e)}")
    
    @retry()
    def automatic_speech_recognition(
        self,
        audio: bytes,
        model: str = Config.DEFAULT_STT_MODEL,
    ) -> dict[str, Any]:
        """
        logger.debug(f"Entering automatic_speech_recognition with model: {model}")
        Convert speech to text.
        
        Args:
            audio: Audio bytes (WAV, MP3, etc.)
            model: Model to use for STT
            
        Returns:
            dict: Transcription result with 'text' and other metadata
            
        Raises:
            HuggingFaceAPIError: If the API call fails
            TimeoutError: If the request times out
        """
        try:
            logger.info(
                f"Converting speech to text with model {model}",
                extra={"audio_size": len(audio), "model": model}
            )
            
            result = self.client.automatic_speech_recognition(
                audio=audio,
                model=model,
            )
            
            logger.debug(f"Exiting automatic_speech_recognition successfully with model {model}")
            return result
        
        except TimeoutError as e:
            logger.error(f"Timeout converting speech to text with model {model}: {str(e)}")
            raise TimeoutError(f"Speech-to-text timed out: {str(e)}", Config.REQUEST_TIMEOUT)
        
        except Exception as e:
            logger.error(f"Error converting speech to text with model {model}: {str(e)}")
            raise HuggingFaceAPIError(f"Failed to convert speech to text: {str(e)}")
    
    @retry()
    def text_generation(
        self,
        prompt: str,
        model: str = Config.DEFAULT_LLM_MODEL,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
    ) -> str:
        """
        logger.debug(f"Entering text_generation with model: {model}")
        Generate text from a prompt.

        Args:
            prompt: Text prompt for generation
            model: Model to use for generation
            max_new_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter

        Returns:
            str: Generated text

        Raises:
            HuggingFaceAPIError: If the API call fails
            TimeoutError: If the request times out
        """
        try:
            logger.info(
                f"Generating text with model {model}",
                extra={"prompt": prompt[:100], "model": model}
            )

            result = self.client.text_generation(
                prompt=prompt,
                model=model,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
            )

            logger.debug(f"Exiting text_generation successfully with model {model}")
            return result

        except TimeoutError as e:
            logger.error(f"Timeout generating text with model {model}: {str(e)}")
            raise TimeoutError(f"Text generation timed out: {str(e)}", Config.REQUEST_TIMEOUT)

        except Exception as e:
            logger.error(f"Error generating text with model {model}: {str(e)}")
            raise HuggingFaceAPIError(f"Failed to generate text: {str(e)}")

    @retry()
    def text_to_video(
        self,
        prompt: str,
        model: str = Config.DEFAULT_TEXT_TO_VIDEO_MODEL,
        negative_prompt: Optional[str] = None,
        duration: int = 8,
        fps: int = 24,
        num_inference_steps: int = 50,
    ) -> bytes:
        """
        logger.debug(f"Entering text_to_video with model: {model}")
        Generate a video from a text prompt.
        
        Args:
            prompt: Text description of the video to generate
            model: Model to use for generation
            negative_prompt: Text to exclude from generation
            duration: Video duration in seconds
            fps: Frames per second
            num_inference_steps: Number of inference steps
            
        Returns:
            bytes: Generated video as MP4 binary data
            
        Raises:
            HuggingFaceAPIError: If the API call fails
            TimeoutError: If the request times out
        """
        provider = get_provider_for_model(model)
        try:
            logger.info(
                f"Generating text-to-video with model {model} (Provider: {provider})",
                extra={"prompt": prompt[:100], "model": model, "provider": provider}
            )
            
            video = self.client.text_to_video(
                prompt=prompt,
                model=model,
                negative_prompt=negative_prompt,
                duration=duration,
                fps=fps,
                num_inference_steps=num_inference_steps,
                provider=provider, # Pass the provider if required
            )
            
            logger.debug(f"Exiting video generation successfully with model {model}")
            return video
        
        except TimeoutError as e:
            logger.error(f"Timeout generating text-to-video with model {model}: {str(e)}")
            raise TimeoutError(f"Text-to-video timed out: {str(e)}", Config.REQUEST_TIMEOUT)
        
        except Exception as e:
            logger.error(f"Error generating text-to-video with model {model}: {str(e)}")
            raise HuggingFaceAPIError(f"Failed to generate text-to-video: {str(e)}")

    @retry()
    def image_to_video(
        self,
        image: bytes,
        model: str = Config.DEFAULT_IMAGE_TO_VIDEO_MODEL,
        prompt: Optional[str] = None,
        duration: int = 6,
        fps: int = 24,
        num_inference_steps: int = 50,
    ) -> bytes:
        """
        logger.debug(f"Entering image_to_video with model: {model}")
        Generate a video from an image.
        
        Args:
            image: Image bytes (PNG, JPG, etc.)
            model: Model to use for generation
            prompt: Optional text prompt for video style
            duration: Video duration in seconds
            fps: Frames per second
            num_inference_steps: Number of inference steps
            
        Returns:
            bytes: Generated video as MP4 binary data
            
        Raises:
            HuggingFaceAPIError: If the API call fails
            TimeoutError: If the request times out
        """
        provider = get_provider_for_model(model)
        try:
            logger.info(
                f"Generating image-to-video with model {model} (Provider: {provider})",
                extra={"image_size": len(image), "model": model, "provider": provider}
            )
            
            video = self.client.image_to_video(
                image=image,
                model=model,
                prompt=prompt,
                duration=duration,
                fps=fps,
                num_inference_steps=num_inference_steps,
                provider=provider, # Pass the provider if required
            )
            
            logger.debug(f"Exiting video generation successfully with model {model}")
            return video
        
        except TimeoutError as e:
            logger.error(f"Timeout generating image-to-video with model {model}: {str(e)}")
            raise TimeoutError(f"Image-to-video timed out: {str(e)}", Config.REQUEST_TIMEOUT)
        
        except Exception as e:
            logger.error(f"Error generating image-to-video with model {model}: {str(e)}")
            raise HuggingFaceAPIError(f"Failed to generate image-to-video: {str(e)}")
    @retry()
    def feature_extraction(
        self,
        text: str,
        model: str = Config.DEFAULT_EMBEDDING_MODEL,
    ) -> list[float]:
        """
        logger.debug(f"Entering feature_extraction with model: {model}")
        Generate embeddings for text.
        
        Args:
            text: Text to embed
            model: Model to use for embeddings
            
        Returns:
            list[float]: Embedding vector
            
        Raises:
            HuggingFaceAPIError: If the API call fails
            TimeoutError: If the request times out
        """
        try:
            logger.info(
                f"Generating embeddings with model {model}",
                extra={"text": text[:100], "model": model}
            )
            
            embedding = self.client.feature_extraction(
                text=text,
                model=model,
            )
            
            logger.debug(f"Exiting feature_extraction successfully with model {model}")
            return embedding
        
        except TimeoutError as e:
            logger.error(f"Timeout generating embeddings with model {model}: {str(e)}")
            raise TimeoutError(f"Embedding generation timed out: {str(e)}", Config.REQUEST_TIMEOUT)
        
        except Exception as e:
            logger.error(f"Error generating embeddings with model {model}: {str(e)}")
            raise HuggingFaceAPIError(f"Failed to generate embeddings: {str(e)}")


# Global service instance
_hf_client: Optional[HuggingFaceClient] = None


def get_hf_client() -> HuggingFaceClient:
    """
    Get or create the global HuggingFace client instance.
    
    Returns:
        HuggingFaceClient: The global client instance
    """
    global _hf_client
    if _hf_client is None:
        _hf_client = HuggingFaceClient()
    return _hf_client
