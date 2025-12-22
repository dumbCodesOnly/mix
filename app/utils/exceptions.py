"""
Custom exception classes for the AI Platform backend.

These exceptions are used throughout the application for consistent
error handling and reporting.
"""

from typing import Any, Optional


class AIServiceException(Exception):
    """Base exception for all AI service errors."""
    
    def __init__(
        self,
        message: str,
        error_code: str = "internal_error",
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None
    ):
        """
        Initialize the exception.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AIServiceException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="validation_error",
            status_code=422,
            details=details
        )


class ModelNotFoundError(AIServiceException):
    """Raised when a requested model is not found or unavailable."""
    
    def __init__(self, model_name: str, service: str):
        super().__init__(
            message=f"Model '{model_name}' not found for service '{service}'",
            error_code="model_not_found",
            status_code=404,
            details={"model": model_name, "service": service}
        )


class HuggingFaceAPIError(AIServiceException):
    """Raised when HuggingFace API returns an error."""
    
    def __init__(self, message: str, status_code: int = 500, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="huggingface_api_error",
            status_code=status_code,
            details=details
        )


class ProcessingError(AIServiceException):
    """Raised when image or audio processing fails."""
    
    def __init__(self, message: str, process_type: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="processing_error",
            status_code=500,
            details={**(details or {}), "process_type": process_type}
        )


class TimeoutError(AIServiceException):
    """Raised when a request times out."""
    
    def __init__(self, message: str, timeout_seconds: int):
        super().__init__(
            message=message,
            error_code="timeout_error",
            status_code=504,
            details={"timeout_seconds": timeout_seconds}
        )


class RateLimitError(AIServiceException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(
            message=message,
            error_code="rate_limit_error",
            status_code=429,
            details={"retry_after": retry_after}
        )


class FileSizeError(AIServiceException):
    """Raised when a file exceeds size limits."""
    
    def __init__(self, file_size: int, max_size: int, file_type: str):
        super().__init__(
            message=f"{file_type} file size {file_size} bytes exceeds maximum {max_size} bytes",
            error_code="file_size_error",
            status_code=413,
            details={
                "file_size": file_size,
                "max_size": max_size,
                "file_type": file_type
            }
        )


class InvalidFormatError(AIServiceException):
    """Raised when file format is invalid."""
    
    def __init__(self, file_type: str, provided_format: str, supported_formats: list[str]):
        super().__init__(
            message=f"Invalid {file_type} format '{provided_format}'. Supported formats: {', '.join(supported_formats)}",
            error_code="invalid_format_error",
            status_code=400,
            details={
                "file_type": file_type,
                "provided_format": provided_format,
                "supported_formats": supported_formats
            }
        )
