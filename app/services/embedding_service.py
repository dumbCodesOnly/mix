"""
Embeddings service.

This module handles generating text embeddings using HuggingFace models.
"""

from typing import Optional

from app.services.hf_client import get_hf_client
from app.utils.config import Config
from app.utils.exceptions import HuggingFaceAPIError, ProcessingError
from app.utils.logging import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """Service for generating text embeddings."""
    
    def __init__(self):
        """Initialize the embedding service."""
        self.hf_client = get_hf_client()
    
    def embed(
        self,
        text: str,
        model: Optional[str] = None,
    ) -> dict:
        """
        Generate embeddings for text.
        
        Args:
            text: Text to embed
            model: Model to use (uses default if None)
            
        Returns:
            dict: Embedding result with 'embedding' vector and metadata
            
        Raises:
            HuggingFaceAPIError: If embedding fails
            ProcessingError: If text processing fails
        """
        model = model or Config.DEFAULT_EMBEDDING_MODEL
        
        try:
            logger.info(
                f"Generating embeddings with model {model}",
                extra={"text_length": len(text), "model": model}
            )
            
            # Call HuggingFace API
            embedding = self.hf_client.feature_extraction(
                text=text,
                model=model,
            )
            
            # Handle different response formats
            if isinstance(embedding, list) and len(embedding) > 0:
                if isinstance(embedding[0], list):
                    # Multiple embeddings, take the first one
                    embedding = embedding[0]
            
            logger.info(
                f"Embeddings generated successfully",
                extra={"embedding_dimension": len(embedding), "model": model}
            )
            
            return {
                "embedding": embedding,
                "dimension": len(embedding),
                "model": model,
                "tokens_used": None,
            }
        
        except HuggingFaceAPIError:
            raise
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise ProcessingError(f"Failed to generate embeddings: {str(e)}", "embedding")


# Global service instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """
    Get or create the global embedding service instance.
    
    Returns:
        EmbeddingService: The global service instance
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
