"""
HuggingFace Inference API client wrapper.

This module provides a centralized interface to the HuggingFace Inference API,
with support for retry logic, model fallback, and comprehensive error handling.
"""

# CRITICAL: Set the HuggingFace inference endpoint BEFORE importing InferenceClient
# HuggingFace has deprecated api-inference.huggingface.co and now requires router.huggingface.co
import os
os.environ['HF_INFERENCE_ENDPOINT'] = 'https://router.huggingface.co'

from typing import Any, Optional

from huggingface_hub import InferenceClient

from app.utils.config import Config
from app.utils.exceptions import HuggingFaceAPIError, ModelNotFoundError, TimeoutError
from app.utils.logging import get_logger
from app.utils.retry import retry

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
            )
            
            # Convert PIL Image to bytes
            import io
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            
            logger.info(f"Image generated successfully with model {model}")
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
            )
            
            # Convert PIL Image to bytes
            import io
            image_bytes = io.BytesIO()
            result.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            
            logger.info(f"Image transformed successfully with model {model}")
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
        model: str = Config.DEFAULT_IMAGE_EDIT_MODEL,
        negative_prompt: Optional[str] = None,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
    ) -> bytes:
        """
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
            )
            
            # Convert PIL Image to bytes
            import io
            image_bytes = io.BytesIO()
            result.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            
            logger.info(f"Image inpainted successfully with model {model}")
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
            
            audio = self.client.text_to_speech(
                text=text,
                model=model,
            )
            
            logger.info(f"Text converted to speech successfully with model {model}")
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
            
            logger.info(f"Speech converted to text successfully with model {model}")
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
        Generate text using a language model.
        
        Args:
            prompt: Input prompt for text generation
            model: Model to use for generation
            max_new_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling
            top_p: Top-p sampling parameter
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
            
            logger.info(f"Text generated successfully with model {model}")
            return result
        
        except TimeoutError as e:
            logger.error(f"Timeout generating text with model {model}: {str(e)}")
            raise TimeoutError(f"Text generation timed out: {str(e)}", Config.REQUEST_TIMEOUT)
        
        except Exception as e:
            logger.error(f"Error generating text with model {model}: {str(e)}")
            raise HuggingFaceAPIError(f"Failed to generate text: {str(e)}")
    
    @retry()
    def feature_extraction(
        self,
        text: str,
        model: str = Config.DEFAULT_EMBEDDING_MODEL,
    ) -> list[float]:
        """
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
            
            logger.info(f"Embeddings generated successfully with model {model}")
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
