"""Video generation API routers.

Provides endpoints for:
- Text-to-video generation
- Image-to-video generation
"""

import base64
import time
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

from app.services.video_service import get_video_service
from app.utils.validation import (
    TextToVideoRequest,
    ImageToVideoRequest,
    VideoGenerationResponse,
    ErrorResponse,
)
from app.utils.exceptions import (
    ValidationError,
    HuggingFaceAPIError,
    ProcessingError,
    FileSizeError,
    ModelNotFoundError,
)
from app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/video", tags=["video"])
video_service = get_video_service()


@router.post(
    "/text-to-video",
    response_class=StreamingResponse,
    responses={
        200: {"description": "Video generated successfully"},
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Generate video from text prompt",
    description="Generate a video from a text description using HuggingFace models.",
)
async def text_to_video(
    request: TextToVideoRequest,
) -> StreamingResponse:
    """Generate video from text prompt.
    
    Args:
        request: TextToVideoRequest containing:
            - prompt: Text description of video
            - model: Optional HuggingFace model ID
            - negative_prompt: Optional negative prompt
            - duration: Video duration (1-30 seconds)
            - fps: Frames per second (1-60)
            - num_inference_steps: Quality/speed tradeoff (1-100)
            
    Returns:
        StreamingResponse: MP4 video file
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        logger.info(
            "Text-to-video request received",
            extra={
                "prompt_length": len(request.prompt),
                "model": request.model,
            },
        )

        # Generate video
        video_data = await video_service.generate_text_to_video(
            prompt=request.prompt,
            model=request.model,
            negative_prompt=request.negative_prompt,
            duration=request.duration,
            fps=request.fps,
            num_inference_steps=request.num_inference_steps,
        )

        # Return video as streaming response
        return StreamingResponse(
            iter([video_data["video_bytes"]]),
            media_type="video/mp4",
            headers={
                "Content-Disposition": 'attachment; filename="video.mp4"',
                "X-Video-Model": video_data["model"],
                "X-Generation-Time": str(video_data["generation_time"]),
            },
        )

    except ValidationError as e:
        logger.warning(f"Validation error in text-to-video: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail={
                "error": "validation_error",
                "message": str(e),
                "details": e.details,
            },
        )
    except ModelNotFoundError as e:
        logger.warning(f"Model not found in text-to-video: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail={
                "error": "model_not_found",
                "message": str(e),
                "details": e.details,
            },
        )
    except FileSizeError as e:
        logger.warning(f"File size error in text-to-video: {str(e)}")
        raise HTTPException(
            status_code=413,
            detail={
                "error": "file_size_error",
                "message": str(e),
                "details": e.details,
            },
        )
    except HuggingFaceAPIError as e:
        logger.error(f"HuggingFace API error in text-to-video: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail={
                "error": "huggingface_api_error",
                "message": str(e),
                "details": e.details,
            },
        )
    except ProcessingError as e:
        logger.error(f"Processing error in text-to-video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "processing_error",
                "message": str(e),
                "details": e.details,
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error in text-to-video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_server_error",
                "message": "An unexpected error occurred",
            },
        )


@router.post(
    "/image-to-video",
    response_class=StreamingResponse,
    responses={
        200: {"description": "Video generated successfully"},
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Generate video from image",
    description="Generate a video from an image using HuggingFace models.",
)
async def image_to_video(
    image: UploadFile = File(..., description="Input image file"),
    model: Optional[str] = Form(
        None, description="HuggingFace model ID"
    ),
    prompt: Optional[str] = Form(
        None, description="Optional text prompt for video style"
    ),
    duration: int = Form(6, ge=1, le=30, description="Video duration in seconds"),
    fps: int = Form(8, ge=1, le=60, description="Frames per second"),
    num_inference_steps: int = Form(
        50, ge=1, le=100, description="Inference steps for quality"
    ),
) -> StreamingResponse:
    """Generate video from image.
    
    Args:
        image: Image file (PNG, JPG, WebP)
        model: Optional HuggingFace model ID
        prompt: Optional text prompt for video style
        duration: Video duration (1-30 seconds)
        fps: Frames per second (1-60)
        num_inference_steps: Quality/speed tradeoff (1-100)
            
    Returns:
        StreamingResponse: MP4 video file
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        # Read image data
        image_data = await image.read()

        logger.info(
            "Image-to-video request received",
            extra={
                "image_size": len(image_data),
                "model": model,
            },
        )

        # Generate video
        video_data = await video_service.generate_image_to_video(
            image_data=image_data,
            model=model,
            prompt=prompt,
            duration=duration,
            fps=fps,
            num_inference_steps=num_inference_steps,
        )

        # Return video as streaming response
        return StreamingResponse(
            iter([video_data["video_bytes"]]),
            media_type="video/mp4",
            headers={
                "Content-Disposition": 'attachment; filename="video.mp4"',
                "X-Video-Model": video_data["model"],
                "X-Generation-Time": str(video_data["generation_time"]),
            },
        )

    except ValidationError as e:
        logger.warning(f"Validation error in image-to-video: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail={
                "error": "validation_error",
                "message": str(e),
                "details": e.details,
            },
        )
    except ModelNotFoundError as e:
        logger.warning(f"Model not found in image-to-video: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail={
                "error": "model_not_found",
                "message": str(e),
                "details": e.details,
            },
        )
    except FileSizeError as e:
        logger.warning(f"File size error in image-to-video: {str(e)}")
        raise HTTPException(
            status_code=413,
            detail={
                "error": "file_size_error",
                "message": str(e),
                "details": e.details,
            },
        )
    except HuggingFaceAPIError as e:
        logger.error(f"HuggingFace API error in image-to-video: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail={
                "error": "huggingface_api_error",
                "message": str(e),
                "details": e.details,
            },
        )
    except ProcessingError as e:
        logger.error(f"Processing error in image-to-video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "processing_error",
                "message": str(e),
                "details": e.details,
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error in image-to-video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_server_error",
                "message": "An unexpected error occurred",
            },
        )
