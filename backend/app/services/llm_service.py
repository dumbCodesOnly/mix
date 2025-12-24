"""
Large Language Model service.

This module handles text generation using HuggingFace models.
"""

from typing import Optional

from app.services.hf_client import get_hf_client
from app.utils.config import Config
from app.utils.exceptions import HuggingFaceAPIError, ProcessingError
from app.utils.logging import get_logger
from app.utils.validation import Message

logger = get_logger(__name__)


class LLMService:
    """Service for large language model text generation."""
    
    def __init__(self):
        """Initialize the LLM service."""
        self.hf_client = get_hf_client()
    
    def generate(
        self,
        messages: list[Message],
        model: Optional[str] = None,
        max_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
    ) -> dict:
        """
        Generate text based on conversation messages.
        
        Args:
            messages: List of Message objects with role and content
            model: Model to use (uses default if None)
            max_tokens: Maximum tokens in response
            temperature: Temperature for sampling
            top_p: Top-p sampling parameter
            top_k: Top-k sampling parameter
            
        Returns:
            dict: Generation result with 'response' and metadata
            
        Raises:
            HuggingFaceAPIError: If generation fails
            ProcessingError: If text processing fails
        """
        model = model or Config.DEFAULT_LLM_MODEL
        
        try:
            # Build prompt from messages
            prompt = self._build_prompt(messages)
            
            logger.info(
                f"Generating text with model {model}",
                extra={"prompt_length": len(prompt), "model": model}
            )
            
            # Call HuggingFace API
            response = self.hf_client.text_generation(
                prompt=prompt,
                model=model,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
            )
            
            logger.info(
                f"Text generated successfully",
                extra={"response_length": len(response), "model": model}
            )
            
            return {
                "response": response,
                "model": model,
                "tokens_used": None,  # Would need to count tokens
                "stop_reason": "length",
            }
        
        except HuggingFaceAPIError:
            raise
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise ProcessingError(f"Failed to generate text: {str(e)}", "llm")
    
    @staticmethod
    def _build_prompt(messages: list[Message]) -> str:
        """
        Build a prompt string from conversation messages using a simple chat template.
        
        Note: For Llama 3.1, the official chat template should be used for best results,
        but a simple turn-based format is used here for compatibility with the Inference API's
        text_generation method, which expects a single string prompt.
        
        Args:
            messages: List of Message objects
            
        Returns:
            str: Formatted prompt string
        """
        prompt_parts = []
        
        for msg in messages:
            if msg.role == "system":
                # System messages are often prepended to the first user message in Llama
                prompt_parts.append(f"<|system|>\n{msg.content}<|end|>")
            elif msg.role == "user":
                prompt_parts.append(f"<|user|>\n{msg.content}<|end|>")
            elif msg.role == "assistant":
                prompt_parts.append(f"<|assistant|>\n{msg.content}<|end|>")
        
        # Add final assistant turn to prompt the model for a response
        prompt_parts.append("<|assistant|>")
        
        return "\n".join(prompt_parts)


# Global service instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """
    Get or create the global LLM service instance.
    
    Returns:
        LLMService: The global service instance
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
