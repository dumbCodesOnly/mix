"""
Configuration management for the AI Platform backend.

This module handles loading and validating environment variables,
providing centralized configuration for the entire application.
"""

import os
from dotenv import load_dotenv

load_dotenv()
from typing import Optional


class Config:
    """Application configuration loaded from environment variables."""

    # HuggingFace API Configuration
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # CORS Configuration
    _allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8081")
    # Handle wildcard for development
    if _allowed_origins_str.strip() == "*":
        ALLOWED_ORIGINS: list[str] = ["*"]
    else:
        ALLOWED_ORIGINS: list[str] = [
            origin.strip() 
            for origin in _allowed_origins_str.split(",")
        ]
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")
    
    # API Configuration
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "300"))  # 5 minutes
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_BACKOFF_MULTIPLIER: float = float(os.getenv("RETRY_BACKOFF_MULTIPLIER", "2.0"))
    INITIAL_RETRY_DELAY: float = float(os.getenv("INITIAL_RETRY_DELAY", "1.0"))
    MAX_RETRY_DELAY: float = float(os.getenv("MAX_RETRY_DELAY", "30.0"))
    
    # Image Processing Configuration
    MAX_IMAGE_SIZE: int = int(os.getenv("MAX_IMAGE_SIZE", "10485760"))  # 10MB
    IMAGE_RESIZE_THRESHOLD: int = int(os.getenv("IMAGE_RESIZE_THRESHOLD", "1024"))
    IMAGE_QUALITY: int = int(os.getenv("IMAGE_QUALITY", "85"))
    
    # Audio Processing Configuration
    MAX_AUDIO_SIZE: int = int(os.getenv("MAX_AUDIO_SIZE", "52428800"))  # 50MB
    
    # Model Configuration
    DEFAULT_TTS_MODEL: str = os.getenv("DEFAULT_TTS_MODEL", "espnet/kan-bayashi_ljspeech_vits")
    DEFAULT_STT_MODEL: str = os.getenv("DEFAULT_STT_MODEL", "openai/whisper-base")
    DEFAULT_IMAGE_MODEL: str = os.getenv("DEFAULT_IMAGE_MODEL", "stabilityai/stable-diffusion-3-medium")
    DEFAULT_IMAGE_EDIT_MODEL: str = os.getenv("DEFAULT_IMAGE_EDIT_MODEL", "stabilityai/stable-diffusion-xl-inpainting")
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")
    DEFAULT_EMBEDDING_MODEL: str = os.getenv("DEFAULT_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Fallback Models
    TTS_FALLBACK_MODELS: list[str] = [
        "microsoft/speecht5_tts",
        "espnet/kan-bayashi_ljspeech_vits"
    ]
    
    STT_FALLBACK_MODELS: list[str] = [
        "openai/whisper-small",
        "openai/whisper-base",
        "openai/whisper-medium"
    ]
    
    IMAGE_FALLBACK_MODELS: list[str] = [
        "black-forest-labs/FLUX.1-dev",
        "runwayml/stable-diffusion-v1-5",
        "stabilityai/stable-diffusion-3-medium"
    ]
    
    IMAGE_EDIT_FALLBACK_MODELS: list[str] = [
        "runwayml/stable-diffusion-inpainting",
        "stabilityai/stable-diffusion-xl-inpainting"
    ]
    
    LLM_FALLBACK_MODELS: list[str] = [
        "mistralai/Mistral-7B-Instruct-v0.1",
        "HuggingFaceH4/zephyr-7b-beta",
        "tiiuae/falcon-7b-instruct"
    ]
    
    EMBEDDING_FALLBACK_MODELS: list[str] = [
        "sentence-transformers/all-mpnet-base-v2",
        "sentence-transformers/all-MiniLM-L6-v2"
    ]

    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required configuration is present.
        
        Returns:
            bool: True if all required config is valid, False otherwise.
            
        Raises:
            ValueError: If required configuration is missing.
        """
        if not cls.HF_API_KEY:
            raise ValueError("HF_API_KEY environment variable is required")
        
        if cls.PORT < 1 or cls.PORT > 65535:
            raise ValueError(f"PORT must be between 1 and 65535, got {cls.PORT}")
        
        if cls.LOG_LEVEL not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"Invalid LOG_LEVEL: {cls.LOG_LEVEL}")
        
        return True

    @classmethod
    def to_dict(cls) -> dict:
        """
        Convert configuration to dictionary.
        
        Returns:
            dict: Configuration as dictionary (excluding sensitive values).
        """
        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "debug": cls.DEBUG,
            "allowed_origins": cls.ALLOWED_ORIGINS,
            "log_level": cls.LOG_LEVEL,
            "request_timeout": cls.REQUEST_TIMEOUT,
            "max_retries": cls.MAX_RETRIES,
            "default_models": {
                "tts": cls.DEFAULT_TTS_MODEL,
                "stt": cls.DEFAULT_STT_MODEL,
                "image": cls.DEFAULT_IMAGE_MODEL,
                "image_edit": cls.DEFAULT_IMAGE_EDIT_MODEL,
                "llm": cls.DEFAULT_LLM_MODEL,
                "embedding": cls.DEFAULT_EMBEDDING_MODEL,
            }
        }


# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    raise RuntimeError(f"Configuration validation failed: {e}")
