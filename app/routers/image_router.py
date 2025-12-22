"""
Image generation and editing router.

This module provides endpoints for text-to-image generation and image editing/inpainting.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import io

from app.services.image_service import get_image_service
from app.utils.exceptions import AIServiceException
from app.utils.logging import get_logger
from app.utils.validation import ImageEditingRequest, ImageGenerationRequest

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["image"])


@router.post("/image")
async def generate_image(request: ImageGenerationRequest):
    """
    Generate an image from a text prompt.
    
    Args:
        request: ImageGenerationRequest with prompt and optional parameters
        
    Returns:
        PNG image as binary data
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        service = get_image_service()
        
        image_bytes = service.generate_image(
            prompt=request.prompt,
            model=request.model,
            negative_prompt=request.negative_prompt,
            height=request.height,
            width=request.width,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
        )
        
        return StreamingResponse(
            io.BytesIO(image_bytes),
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=generated_image.png"}
        )
    
    except AIServiceException as e:
        logger.error(f"Image generation error: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except Exception as e:
        logger.error(f"Unexpected error in image generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/edit-image")
async def edit_image(request: ImageEditingRequest):
    """
    Edit an image based on a text prompt.
    
    Supports both inpainting (with mask) and image-to-image transformation.
    
    Args:
        request: ImageEditingRequest with image, prompt, and optional mask
        
    Returns:
        PNG image as binary data
        
    Raises:
        HTTPException: If editing fails
    """
    try:
        service = get_image_service()
        
        image_bytes = service.edit_image(
            image_data=request.image,
            prompt=request.prompt,
            mask_data=request.mask,
            model=request.model,
            negative_prompt=request.negative_prompt,
            strength=request.strength,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
        )
        
        return StreamingResponse(
            io.BytesIO(image_bytes),
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=edited_image.png"}
        )
    
    except AIServiceException as e:
        logger.error(f"Image editing error: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    
    except Exception as e:
        logger.error(f"Unexpected error in image editing: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
