"""
Image generation and processing service.

This module handles text-to-image generation with resizing,
compression, and optimization for efficient transmission.
"""

import base64
import io
from typing import Optional

from PIL import Image

from app.services.hf_client import get_hf_client
from app.utils.config import Config
from app.utils.exceptions import (
    FileSizeError,
    HuggingFaceAPIError,
    InvalidFormatError,
    ProcessingError,
)
from app.utils.logging import get_logger
from app.utils.retry import retry_with_fallback

logger = get_logger(__name__)


class ImageService:
    """Service for image generation and processing."""
    
    SUPPORTED_FORMATS = {"PNG", "JPEG", "JPG"}
    MAX_DIMENSION = 1024
    MIN_DIMENSION = 256
    
    def __init__(self):
        """Initialize the image service."""
        self.hf_client = get_hf_client()
    
    @staticmethod
    def decode_base64_image(image_data: str) -> Image.Image:
        """
        Decode a base64-encoded image string.
        
        Args:
            image_data: Base64-encoded image string
            
        Returns:
            Image.Image: Decoded PIL Image
            
        Raises:
            InvalidFormatError: If the image format is invalid
            ProcessingError: If decoding fails
        """
        try:
            # Remove data URI prefix if present
            if "," in image_data:
                image_data = image_data.split(",", 1)[1]
            
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            return image
        except Exception as e:
            logger.error(f"Failed to decode base64 image: {str(e)}")
            raise ProcessingError(f"Failed to decode image: {str(e)}", "image_decoding")
    
    @staticmethod
    def encode_image_to_base64(image: Image.Image, format: str = "PNG") -> str:
        """
        Encode a PIL Image to base64 string.
        
        Args:
            image: PIL Image to encode
            format: Image format (PNG, JPEG, etc.)
            
        Returns:
            str: Base64-encoded image string
            
        Raises:
            ProcessingError: If encoding fails
        """
        try:
            image_bytes = io.BytesIO()
            image.save(image_bytes, format=format)
            image_bytes.seek(0)
            
            encoded = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
            return encoded
        except Exception as e:
            logger.error(f"Failed to encode image to base64: {str(e)}")
            raise ProcessingError(f"Failed to encode image: {str(e)}", "image_encoding")
    
    @staticmethod
    def image_to_bytes(image: Image.Image, format: str = "PNG", quality: Optional[int] = None) -> bytes:
        """
        Convert a PIL Image to bytes.
        
        Args:
            image: PIL Image to convert
            format: Image format (PNG, JPEG, etc.)
            quality: JPEG quality (1-100, only for JPEG)
            
        Returns:
            bytes: Image as binary data
            
        Raises:
            ProcessingError: If conversion fails
        """
        try:
            image_bytes = io.BytesIO()
            
            if format.upper() == "JPEG" and quality:
                image.save(image_bytes, format=format, quality=quality)
            else:
                image.save(image_bytes, format=format)
            
            image_bytes.seek(0)
            return image_bytes.getvalue()
        except Exception as e:
            logger.error(f"Failed to convert image to bytes: {str(e)}")
            raise ProcessingError(f"Failed to convert image: {str(e)}", "image_conversion")
    
    @staticmethod
    def resize_image(
        image: Image.Image,
        max_dimension: int = Config.IMAGE_RESIZE_THRESHOLD
    ) -> Image.Image:
        """
        Resize an image if it exceeds the maximum dimension.
        
        Args:
            image: PIL Image to resize
            max_dimension: Maximum width or height
            
        Returns:
            Image.Image: Resized image (or original if smaller)
        """
        width, height = image.size
        
        if width <= max_dimension and height <= max_dimension:
            return image
        
        # Calculate new dimensions maintaining aspect ratio
        if width > height:
            new_width = max_dimension
            new_height = int(height * (max_dimension / width))
        else:
            new_height = max_dimension
            new_width = int(width * (max_dimension / height))
        
        logger.info(
            f"Resizing image from {width}x{height} to {new_width}x{new_height}",
            extra={"original_size": (width, height), "new_size": (new_width, new_height)}
        )
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def generate_image(
        self,
        prompt: str,
        model: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        height: int = 512,
        width: int = 512,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
    ) -> bytes:
        """
        Generate an image from a text prompt.
        
        Args:
            prompt: Text description of the image
            model: Model to use (uses default if None)
            negative_prompt: Text to exclude from generation
            height: Image height in pixels
            width: Image width in pixels
            num_inference_steps: Number of inference steps
            guidance_scale: Guidance scale for prompt adherence
            
        Returns:
            bytes: Generated image as PNG binary data
            
        Raises:
            HuggingFaceAPIError: If generation fails
            ProcessingError: If image processing fails
        """
        model = model or Config.DEFAULT_IMAGE_MODEL
        
        try:
            logger.info(f"Generating image with prompt: {prompt[:100]}")
            
            # Generate image
            image_bytes = self.hf_client.text_to_image(
                prompt=prompt,
                model=model,
                negative_prompt=negative_prompt,
                height=height,
                width=width,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
            )
            
            # Convert to PIL Image for processing
            image = Image.open(io.BytesIO(image_bytes))
            
            # Resize if needed
            image = self.resize_image(image)
            
            # Convert to bytes with optimization
            output_bytes = self.image_to_bytes(image, format="PNG")
            
            logger.info(f"Image generated successfully, size: {len(output_bytes)} bytes")
            return output_bytes
        
        except HuggingFaceAPIError:
            raise
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise ProcessingError(f"Failed to generate image: {str(e)}", "image_generation")
    
    def edit_image(
        self,
        image_data: str,
        prompt: str,
        mask_data: Optional[str] = None,
        model: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        strength: float = 0.75,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
    ) -> bytes:
        """
        Edit an image based on a text prompt.
        
        Args:
            image_data: Base64-encoded original image
            prompt: Text description for the edit
            mask_data: Base64-encoded mask (optional, for inpainting)
            model: Model to use (uses default if None)
            negative_prompt: Text to exclude from generation
            strength: Strength of the edit (0-1)
            num_inference_steps: Number of inference steps
            guidance_scale: Guidance scale for prompt adherence
            
        Returns:
            bytes: Edited image as PNG binary data
            
        Raises:
            HuggingFaceAPIError: If editing fails
            ProcessingError: If image processing fails
        """
        model = model or Config.DEFAULT_IMAGE_EDIT_MODEL
        
        try:
            logger.info(f"Editing image with prompt: {prompt[:100]}")
            
            # Decode original image
            image = self.decode_base64_image(image_data)
            
            # Resize if needed
            image = self.resize_image(image)
            
            # Handle inpainting with mask
            if mask_data:
                mask = self.decode_base64_image(mask_data)
                mask = self.resize_image(mask)
                
                # Perform inpainting
                output_bytes = self.hf_client.inpainting(
                    image=image,
                    mask=mask,
                    prompt=prompt,
                    model=model,
                    negative_prompt=negative_prompt,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                )
            else:
                # Perform image-to-image transformation
                output_bytes = self.hf_client.image_to_image(
                    image=image,
                    prompt=prompt,
                    model=model,
                    negative_prompt=negative_prompt,
                    strength=strength,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                )
            
            # Convert to PIL Image for processing
            result_image = Image.open(io.BytesIO(output_bytes))
            
            # Resize if needed
            result_image = self.resize_image(result_image)
            
            # Convert to bytes with optimization
            final_bytes = self.image_to_bytes(result_image, format="PNG")
            
            logger.info(f"Image edited successfully, size: {len(final_bytes)} bytes")
            return final_bytes
        
        except HuggingFaceAPIError:
            raise
        except Exception as e:
            logger.error(f"Error editing image: {str(e)}")
            raise ProcessingError(f"Failed to edit image: {str(e)}", "image_editing")


# Global service instance
_image_service: Optional[ImageService] = None


def get_image_service() -> ImageService:
    """
    Get or create the global image service instance.
    
    Returns:
        ImageService: The global service instance
    """
    global _image_service
    if _image_service is None:
        _image_service = ImageService()
    return _image_service
