"""API routers for the AI Platform backend."""

from app.routers import embedding_router, health_router, image_router, llm_router, stt_router, tts_router, video_router

__all__ = [
    "health_router",
    "image_router",
    "tts_router",
    "stt_router",
    "llm_router",
    "embedding_router",
    "video_router",
]
