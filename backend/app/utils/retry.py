"""
Retry logic with exponential backoff for API calls.

This module provides decorators and utilities for implementing
robust retry mechanisms with exponential backoff.
"""

import asyncio
import time
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

from app.utils.config import Config
from app.utils.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


def should_retry(exception: Exception) -> bool:
    """
    Determine if an exception should trigger a retry.
    
    Args:
        exception: The exception that occurred
        
    Returns:
        bool: True if the exception is retryable, False otherwise
    """
    # Retry on timeout errors
    if isinstance(exception, TimeoutError):
        return True
    
    # Retry on connection errors
    if isinstance(exception, (ConnectionError, OSError)):
        return True
    
    # Don't retry on validation errors
    if isinstance(exception, ValueError):
        return False
    
    # Retry on generic exceptions (might be transient)
    return True


def retry(
    max_retries: Optional[int] = None,
    initial_delay: Optional[float] = None,
    backoff_multiplier: Optional[float] = None,
    max_delay: Optional[float] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for retrying a function with exponential backoff.
    
    Args:
        max_retries: Maximum number of retries (uses config default if None)
        initial_delay: Initial delay in seconds (uses config default if None)
        backoff_multiplier: Multiplier for exponential backoff (uses config default if None)
        max_delay: Maximum delay between retries (uses config default if None)
        
    Returns:
        Callable: Decorated function with retry logic
    """
    max_retries = max_retries or Config.MAX_RETRIES
    initial_delay = initial_delay or Config.INITIAL_RETRY_DELAY
    backoff_multiplier = backoff_multiplier or Config.RETRY_BACKOFF_MULTIPLIER
    max_delay = max_delay or Config.MAX_RETRY_DELAY
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            delay = initial_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt == max_retries or not should_retry(e):
                        logger.error(
                            f"Function {func.__name__} failed after {attempt + 1} attempts",
                            extra={"error": str(e), "attempt": attempt + 1}
                        )
                        raise
                    
                    # Log retry attempt
                    logger.warning(
                        f"Function {func.__name__} failed on attempt {attempt + 1}, retrying in {delay}s",
                        extra={"error": str(e), "attempt": attempt + 1, "delay": delay}
                    )
                    
                    # Wait before retrying
                    time.sleep(delay)
                    
                    # Calculate next delay with exponential backoff
                    delay = min(delay * backoff_multiplier, max_delay)
            
            # This should never be reached, but just in case
            raise last_exception or RuntimeError("Retry failed for unknown reason")
        
        return wrapper
    
    return decorator


async def async_retry(
    max_retries: Optional[int] = None,
    initial_delay: Optional[float] = None,
    backoff_multiplier: Optional[float] = None,
    max_delay: Optional[float] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for retrying an async function with exponential backoff.
    
    Args:
        max_retries: Maximum number of retries (uses config default if None)
        initial_delay: Initial delay in seconds (uses config default if None)
        backoff_multiplier: Multiplier for exponential backoff (uses config default if None)
        max_delay: Maximum delay between retries (uses config default if None)
        
    Returns:
        Callable: Decorated async function with retry logic
    """
    max_retries = max_retries or Config.MAX_RETRIES
    initial_delay = initial_delay or Config.INITIAL_RETRY_DELAY
    backoff_multiplier = backoff_multiplier or Config.RETRY_BACKOFF_MULTIPLIER
    max_delay = max_delay or Config.MAX_RETRY_DELAY
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            delay = initial_delay
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt == max_retries or not should_retry(e):
                        logger.error(
                            f"Function {func.__name__} failed after {attempt + 1} attempts",
                            extra={"error": str(e), "attempt": attempt + 1}
                        )
                        raise
                    
                    # Log retry attempt
                    logger.warning(
                        f"Function {func.__name__} failed on attempt {attempt + 1}, retrying in {delay}s",
                        extra={"error": str(e), "attempt": attempt + 1, "delay": delay}
                    )
                    
                    # Wait before retrying
                    await asyncio.sleep(delay)
                    
                    # Calculate next delay with exponential backoff
                    delay = min(delay * backoff_multiplier, max_delay)
            
            # This should never be reached, but just in case
            raise last_exception or RuntimeError("Retry failed for unknown reason")
        
        return wrapper
    
    return decorator


def retry_with_fallback(
    fallback_values: list[Any],
    max_retries: Optional[int] = None,
    initial_delay: Optional[float] = None,
    backoff_multiplier: Optional[float] = None,
    max_delay: Optional[float] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for retrying a function with fallback values.
    
    This is useful for trying different models when the primary fails.
    
    Args:
        fallback_values: List of values to try as fallbacks
        max_retries: Maximum number of retries per value
        initial_delay: Initial delay in seconds
        backoff_multiplier: Multiplier for exponential backoff
        max_delay: Maximum delay between retries
        
    Returns:
        Callable: Decorated function with fallback retry logic
    """
    max_retries = max_retries or Config.MAX_RETRIES
    initial_delay = initial_delay or Config.INITIAL_RETRY_DELAY
    backoff_multiplier = backoff_multiplier or Config.RETRY_BACKOFF_MULTIPLIER
    max_delay = max_delay or Config.MAX_RETRY_DELAY
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            
            # Try each fallback value
            for fallback_value in fallback_values:
                delay = initial_delay
                
                for attempt in range(max_retries + 1):
                    try:
                        # Update the first positional argument with fallback value
                        new_args = (fallback_value,) + args[1:] if args else (fallback_value,)
                        return func(*new_args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        
                        if attempt == max_retries or not should_retry(e):
                            logger.warning(
                                f"Fallback value {fallback_value} failed for {func.__name__}",
                                extra={"error": str(e), "fallback": fallback_value}
                            )
                            break
                        
                        # Wait before retrying
                        time.sleep(delay)
                        delay = min(delay * backoff_multiplier, max_delay)
            
            # All fallbacks exhausted
            logger.error(
                f"All fallback values exhausted for {func.__name__}",
                extra={"error": str(last_exception)}
            )
            raise last_exception or RuntimeError("All fallback values failed")
        
        return wrapper
    
    return decorator
