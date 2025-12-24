"""
Main FastAPI application entry point.

This module sets up the FastAPI application with middleware,
exception handlers, and all API routers.
"""

from datetime import datetime
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import (
    config_router,
    embedding_router,
    health_router,
    image_router,
    llm_router,
    stt_router,
    tts_router,
    video_router,
)
from app.utils import AIServiceException, Config, get_logger, setup_logging

# Set up logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Platform Backend",
    description="Production-ready FastAPI service for HuggingFace models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.info(
        f"Incoming request: {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else "unknown",
        }
    )
    
    response = await call_next(request)
    
    logger.info(
        f"Response: {response.status_code}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
        }
    )
    
    return response


# Global exception handler for AIServiceException
@app.exception_handler(AIServiceException)
async def ai_service_exception_handler(request: Request, exc: AIServiceException):
    """Handle AIServiceException and return formatted JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
    )


# Global exception handler for general exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", extra={"exception": str(exc)})
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "An unexpected error occurred",
            "details": {},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
    )


# Register routers
app.include_router(health_router.router)
app.include_router(image_router.router)
app.include_router(tts_router.router)
app.include_router(stt_router.router)
app.include_router(llm_router.router)
app.include_router(embedding_router.router)
app.include_router(video_router.router)
app.include_router(config_router.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AI Platform Backend",
        "version": "1.0.0",
        "description": "Production-ready FastAPI service for HuggingFace models",
        "docs": "/docs",
        "health": "/health",
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("AI Platform Backend starting up")
    logger.info(f"Configuration: {Config.to_dict()}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("AI Platform Backend shutting down")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        log_level=Config.LOG_LEVEL.lower(),
    )
