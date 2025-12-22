"""
Pydantic models for request and response validation.

This module defines all the request/response schemas used by the API,
providing type safety and automatic validation.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Base Models
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp in ISO format")


class ErrorResponse(BaseModel):
    """Error response format."""
    
    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Timestamp in ISO format")


# ============================================================================
# Image Generation Models
# ============================================================================

class ImageGenerationRequest(BaseModel):
    """Request model for text-to-image generation."""
    
    prompt: str = Field(..., min_length=1, max_length=1000, description="Text prompt for image generation")
    model: Optional[str] = Field(None, description="Model to use (optional, uses default if not specified)")
    negative_prompt: Optional[str] = Field(None, max_length=1000, description="Negative prompt to exclude from generation")
    height: Optional[int] = Field(512, ge=256, le=1024, description="Image height in pixels")
    width: Optional[int] = Field(512, ge=256, le=1024, description="Image width in pixels")
    num_inference_steps: Optional[int] = Field(50, ge=1, le=100, description="Number of inference steps")
    guidance_scale: Optional[float] = Field(7.5, ge=1.0, le=20.0, description="Guidance scale for prompt adherence")


# ============================================================================
# Image Editing Models
# ============================================================================

class ImageEditingRequest(BaseModel):
    """Request model for image editing and inpainting."""
    
    image: str = Field(..., description="Base64-encoded original image")
    prompt: str = Field(..., min_length=1, max_length=1000, description="Prompt for image modification")
    mask: Optional[str] = Field(None, description="Base64-encoded mask for inpainting (optional)")
    model: Optional[str] = Field(None, description="Model to use (optional, uses default if not specified)")
    negative_prompt: Optional[str] = Field(None, max_length=1000, description="Negative prompt")
    strength: Optional[float] = Field(0.75, ge=0.0, le=1.0, description="Strength of the edit (0-1)")
    num_inference_steps: Optional[int] = Field(50, ge=1, le=100, description="Number of inference steps")
    
    @field_validator("image", "mask")
    @classmethod
    def validate_base64(cls, v: Optional[str]) -> Optional[str]:
        """Validate that image/mask are valid base64 strings."""
        if v is None:
            return v
        
        # Basic base64 validation
        if not v or len(v) < 100:
            raise ValueError("Image data appears to be invalid or too small")
        
        return v


# ============================================================================
# Text-to-Speech Models
# ============================================================================

class TTSRequest(BaseModel):
    """Request model for text-to-speech."""
    
    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to speech")
    model: Optional[str] = Field(None, description="Model to use (optional, uses default if not specified)")
    speaker_id: Optional[int] = Field(0, ge=0, le=100, description="Speaker ID for multi-speaker models")
    speed: Optional[float] = Field(1.0, ge=0.5, le=2.0, description="Speech speed multiplier")


class TTSResponse(BaseModel):
    """Response model for text-to-speech."""
    
    model: str = Field(..., description="Model used for generation")
    duration: float = Field(..., description="Duration of generated audio in seconds")
    sample_rate: int = Field(..., description="Audio sample rate in Hz")


# ============================================================================
# Speech-to-Text Models
# ============================================================================

class STTRequest(BaseModel):
    """Request model for speech-to-text."""
    
    model: Optional[str] = Field(None, description="Model to use (optional, uses default if not specified)")
    language: Optional[str] = Field(None, description="Language code (e.g., 'en', 'fr')")


class STTResponse(BaseModel):
    """Response model for speech-to-text."""
    
    text: str = Field(..., description="Transcribed text")
    language: Optional[str] = Field(None, description="Detected language")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")
    model: str = Field(..., description="Model used for transcription")


# ============================================================================
# LLM Models
# ============================================================================

class Message(BaseModel):
    """Message in conversation."""
    
    role: str = Field(..., description="Role: 'system', 'user', or 'assistant'")
    content: str = Field(..., description="Message content")


class LLMRequest(BaseModel):
    """Request model for LLM text generation."""
    
    messages: list[Message] = Field(..., min_items=1, description="Conversation messages")
    model: Optional[str] = Field(None, description="Model to use (optional, uses default if not specified)")
    max_tokens: Optional[int] = Field(256, ge=1, le=2048, description="Maximum tokens in response")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Temperature for sampling")
    top_p: Optional[float] = Field(0.9, ge=0.0, le=1.0, description="Top-p sampling parameter")
    top_k: Optional[int] = Field(50, ge=1, le=100, description="Top-k sampling parameter")
    
    @field_validator("messages")
    @classmethod
    def validate_messages(cls, v: list[Message]) -> list[Message]:
        """Validate that messages have valid roles."""
        valid_roles = {"system", "user", "assistant"}
        for msg in v:
            if msg.role not in valid_roles:
                raise ValueError(f"Invalid role '{msg.role}'. Must be one of {valid_roles}")
        return v


class LLMResponse(BaseModel):
    """Response model for LLM text generation."""
    
    response: str = Field(..., description="Generated response text")
    model: str = Field(..., description="Model used for generation")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")
    stop_reason: Optional[str] = Field(None, description="Reason generation stopped")


# ============================================================================
# Embeddings Models
# ============================================================================

class EmbeddingRequest(BaseModel):
    """Request model for embeddings."""
    
    text: str = Field(..., min_length=1, max_length=5000, description="Text to embed")
    model: Optional[str] = Field(None, description="Model to use (optional, uses default if not specified)")


class EmbeddingResponse(BaseModel):
    """Response model for embeddings."""
    
    embedding: list[float] = Field(..., description="Embedding vector")
    dimension: int = Field(..., description="Dimension of embedding vector")
    model: str = Field(..., description="Model used for embedding")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")


# ============================================================================
# Video Generation Models
# ============================================================================

class TextToVideoRequest(BaseModel):
    """Request model for text-to-video generation."""
    
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Text description of the video"
    )
    model: Optional[str] = Field(
        None,
        description="HuggingFace model ID"
    )
    negative_prompt: Optional[str] = Field(
        None,
        max_length=500,
        description="What to avoid in the video"
    )
    duration: int = Field(
        default=6,
        ge=1,
        le=30,
        description="Video duration in seconds"
    )
    fps: int = Field(
        default=8,
        ge=1,
        le=60,
        description="Frames per second"
    )
    num_inference_steps: int = Field(
        default=50,
        ge=1,
        le=100,
        description="Inference steps for quality"
    )


class ImageToVideoRequest(BaseModel):
    """Request model for image-to-video generation."""
    
    image: str = Field(
        ...,
        description="Base64 encoded image data"
    )
    model: Optional[str] = Field(
        None,
        description="HuggingFace model ID"
    )
    prompt: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional text prompt for video style"
    )
    duration: int = Field(
        default=6,
        ge=1,
        le=30,
        description="Video duration in seconds"
    )
    fps: int = Field(
        default=8,
        ge=1,
        le=60,
        description="Frames per second"
    )
    num_inference_steps: int = Field(
        default=50,
        ge=1,
        le=100,
        description="Inference steps for quality"
    )


class VideoGenerationResponse(BaseModel):
    """Response model for video generation."""
    
    video_url: str = Field(
        ...,
        description="URL to download the video"
    )
    video_size: int = Field(
        ...,
        description="Video file size in bytes"
    )
    duration: float = Field(
        ...,
        description="Video duration in seconds"
    )
    fps: int = Field(
        ...,
        description="Frames per second"
    )
    resolution: str = Field(
        ...,
        description="Video resolution"
    )
    model: str = Field(
        ...,
        description="Model used for generation"
    )
    generation_time: float = Field(
        ...,
        description="Time taken to generate in seconds"
    )
    format: str = Field(
        default="mp4",
        description="Video file format"
    )
