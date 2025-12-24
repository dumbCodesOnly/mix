from fastapi import APIRouter
from app.utils.config import Config
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/config", tags=["Configuration"])

@router.get("/models")
async def get_supported_models():
    """
    Returns a list of all supported models grouped by service type.
    """
    logger.debug("Received request for supported models list")
    
    # Helper function to combine default and fallback models
    def get_model_list(default_model: str, fallback_models: list[str]) -> list[str]:
        models = [default_model]
        for model in fallback_models:
            if model not in models:
                models.append(model)
        return models

    response = {
        "llm": get_model_list(Config.DEFAULT_LLM_MODEL, Config.LLM_FALLBACK_MODELS),
        "image": get_model_list(Config.DEFAULT_IMAGE_MODEL, Config.IMAGE_FALLBACK_MODELS),
        "image_edit": get_model_list(Config.DEFAULT_IMAGE_EDIT_MODEL, Config.IMAGE_EDIT_FALLBACK_MODELS),
        "tts": get_model_list(Config.DEFAULT_TTS_MODEL, Config.TTS_FALLBACK_MODELS),
        "stt": get_model_list(Config.DEFAULT_STT_MODEL, Config.STT_FALLBACK_MODELS),
        "text_to_video": get_model_list(Config.DEFAULT_TEXT_TO_VIDEO_MODEL, Config.TEXT_TO_VIDEO_FALLBACK_MODELS),
        "image_to_video": get_model_list(Config.DEFAULT_IMAGE_TO_VIDEO_MODEL, Config.IMAGE_TO_VIDEO_FALLBACK_MODELS),
        "embedding": get_model_list(Config.DEFAULT_EMBEDDING_MODEL, Config.EMBEDDING_FALLBACK_MODELS),
    }
    
    logger.debug("Returning supported models list")
    return response

@router.get("/config")
async def get_public_config():
    """
    Returns public configuration settings (excluding API keys).
    """
    logger.debug("Received request for public configuration")
    return Config.to_dict()
