"""
Logging configuration for the AI Platform backend.

This module sets up structured logging with JSON format support
and configurable log levels.
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Optional

from app.utils.config import Config


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record as JSON.
        
        Args:
            record: The log record to format
            
        Returns:
            str: JSON-formatted log message
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data)


def setup_logging() -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("ai-platform")
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Set formatter based on configuration
    if Config.LOG_FORMAT.lower() == "json":
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: The name of the logger (usually __name__)
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


def log_with_context(
    logger: logging.Logger,
    level: int,
    message: str,
    **extra_fields: Any
) -> None:
    """
    Log a message with additional context fields.
    
    Args:
        logger: The logger instance
        level: The logging level
        message: The log message
        **extra_fields: Additional fields to include in the log
    """
    record = logger.makeRecord(
        name=logger.name,
        level=level,
        fn="",
        lno=0,
        msg=message,
        args=(),
        exc_info=None
    )
    record.extra_fields = extra_fields
    logger.handle(record)


# Initialize logging on module import
logger = setup_logging()
