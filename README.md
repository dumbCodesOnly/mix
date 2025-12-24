# AI Platform Backend

A production-ready FastAPI service for multiple HuggingFace AI models, providing unified APIs for text-to-speech, speech-to-text, image generation, image editing, large language models, and embeddings.

## Features

- **Text-to-Image Generation**: Generate images from text prompts using Stable Diffusion and other models
- **Image Editing & Inpainting**: Edit images with text prompts or draw masks for precise inpainting
- **Text-to-Video Generation**: Generate videos from text descriptions using HuggingFace video models
- **Image-to-Video Generation**: Create videos from static images with optional motion prompts
- **Text-to-Speech**: Convert text to natural-sounding speech in multiple languages
- **Speech-to-Text**: Transcribe audio files with high accuracy using Whisper
- **Large Language Models**: Generate text using state-of-the-art language models
- **Embeddings**: Generate vector embeddings for semantic search and similarity
- **Robust Error Handling**: Comprehensive exception handling with meaningful error messages
- **Retry Logic**: Automatic retry with exponential backoff for transient failures
- **Model Fallback**: Automatic fallback to alternative models if the primary fails
- **Request Logging**: Structured logging for debugging and monitoring
- **CORS Support**: Configured for cross-origin requests from mobile and web clients

## Architecture

```
/app
    main.py                 # FastAPI application entry point
    routers/               # API endpoint definitions
        health_router.py
        image_router.py
        video_router.py
        tts_router.py
        stt_router.py
        llm_router.py
        config_router.py
        embedding_router.py
    services/             # Business logic layer
        hf_client.py      # HuggingFace API wrapper
        image_service.py
        video_service.py
        tts_service.py
        stt_service.py
        llm_service.py
        embedding_service.py
    utils/                # Utility modules
        config.py         # Configuration management
        exceptions.py     # Custom exceptions
        logging.py        # Logging setup
        validation.py     # Pydantic models
        retry.py          # Retry logic
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- HuggingFace API key (get one at https://huggingface.co/settings/tokens)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-platform
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your HuggingFace API key
```

5. Run the server:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

## API Endpoints

### Health Check

**Endpoint:** `GET /health`

Check if the service is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-22T10:30:00Z"
}
```

### Image Generation

**Endpoint:** `POST /api/image`

Generate an image from a text prompt.

**Request:**
```json
{
  "prompt": "A serene landscape with mountains and sunset",
  "model": "stabilityai/stable-diffusion-3-medium",
  "negative_prompt": "blurry, low quality",
  "height": 512,
  "width": 512,
  "num_inference_steps": 50,
  "guidance_scale": 7.5
}
```

**Response:** PNG image binary data

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A serene landscape with mountains",
    "height": 512,
    "width": 512
  }' \
  --output generated_image.png
```

### Image Editing

**Endpoint:** `POST /api/edit-image`

Edit an image using text prompts with optional mask for inpainting.

**Request (Inpainting with mask):**
```json
{
  "image": "base64-encoded-image-data",
  "mask": "base64-encoded-mask-data",
  "prompt": "Make the sky sunset orange",
  "model": "stabilityai/stable-diffusion-xl-inpainting",
  "strength": 0.75
}
```

**Request (Image-to-image without mask):**
```json
{
  "image": "base64-encoded-image-data",
  "prompt": "Convert to oil painting style",
  "strength": 0.75
}
```

**Response:** PNG image binary data

### Text-to-Speech

**Endpoint:** `POST /api/tts`

Convert text to speech.

**Request:**
```json
{
  "text": "Hello, this is a test of text-to-speech",
  "model": "espnet/kan-bayashi_ljspeech_vits",
  "speaker_id": 0,
  "speed": 1.0
}
```

**Response:** WAV audio binary data

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world"
  }' \
  --output speech.wav
```

### Speech-to-Text

**Endpoint:** `POST /api/stt`

Convert speech to text. Accepts audio files via multipart form data.

**Request:**
```
POST /api/stt
Content-Type: multipart/form-data

audio: <binary audio file>
model: openai/whisper-base (optional)
language: en (optional)
```

**Response:**
```json
{
  "text": "Transcribed text from audio",
  "language": "en",
  "confidence": 0.95,
  "model": "openai/whisper-base"
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/stt \
  -F "audio=@audio_file.wav" \
  -F "language=en"
```

### Large Language Model

**Endpoint:** `POST /api/llm`

Generate text using a language model.

**Request:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant"
    },
    {
      "role": "user",
      "content": "What is the capital of France?"
    }
  ],
  "model": "meta-llama/Llama-2-7b-chat-hf",
  "max_tokens": 256,
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 50
}
```

**Response:**
```json
{
  "response": "The capital of France is Paris.",
  "model": "meta-llama/Llama-2-7b-chat-hf",
  "tokens_used": 45,
  "stop_reason": "length"
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/llm \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Embeddings

**Endpoint:** `POST /api/embedding`

Generate embeddings for text.

**Request:**
```json
{
  "text": "Sample text to embed",
  "model": "sentence-transformers/all-MiniLM-L6-v2"
}
```

**Response:**
```json
{
  "embedding": [0.123, -0.456, 0.789, ...],
  "dimension": 384,
  "model": "sentence-transformers/all-MiniLM-L6-v2",
  "tokens_used": 5
}
```

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/embedding \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Sample text to embed"
  }'
```

### Text-to-Video Generation

**Endpoint:** `POST /api/video/text-to-video`

Generate a video from a text description using HuggingFace video models.

**Request:**
```json
{
  "prompt": "A cat walking through a garden",
  "model": "damo-vilab/text-to-video-ms-1.7b",
  "negative_prompt": "blurry, low quality",
  "duration": 8,
  "fps": 24,
  "num_inference_steps": 50
}
```

**Response:** MP4 video binary data

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/video/text-to-video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "duration": 8,
    "fps": 24
  }' \
  --output video.mp4
```

### Image-to-Video Generation

**Endpoint:** `POST /api/video/image-to-video`

Generate a video from a static image with optional motion prompts.

**Request (Multipart form data):**
```
POST /api/video/image-to-video
Content-Type: multipart/form-data

image: <binary image file>
prompt: cinematic camera movement (optional)
fps: 24 (optional)
duration: 6 (optional)
num_inference_steps: 50 (optional)
```

**Response:** MP4 video binary data

**Example with curl:**
```bash
curl -X POST http://localhost:8000/api/video/image-to-video \
  -F "image=@input_image.jpg" \
  -F "prompt=cinematic movement" \
  -F "fps=24" \
  --output video.mp4
```

## Error Handling

All errors follow a consistent JSON format:

```json
{
  "error": "error_code",
  "message": "Human-readable error description",
  "details": {
    "field": "specific_field_error"
  },
  "timestamp": "2025-12-22T10:30:00Z"
}
```

### Common Error Codes

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| `validation_error` | 422 | Invalid input parameters |
| `model_not_found` | 404 | Requested model unavailable |
| `huggingface_api_error` | 500 | Error from HuggingFace API |
| `processing_error` | 500 | Error during image/audio processing |
| `timeout_error` | 504 | Request timeout |
| `rate_limit_error` | 429 | Rate limit exceeded |
| `file_size_error` | 413 | File exceeds size limit |
| `invalid_format_error` | 400 | Invalid file format |

## Configuration
\n### Dynamic Model Configuration
\nModel lists for the frontend (LLM, Image Generation, etc.) are now fetched dynamically from the backend via the `GET /config/models` endpoint. This ensures that the frontend always uses the models configured in the backend's `config.py` file, preventing hardcoding errors and deprecated model usage.
\n\n### Key Configuration Variables

Configuration is managed through environment variables. See `.env.example` for all available options.

### Key Configuration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_API_KEY` | (required) | HuggingFace API key |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |
| `DEBUG` | `false` | Debug mode |
| `ALLOWED_ORIGINS` | `http://localhost:3000,http://localhost:8081` | CORS allowed origins |
| `LOG_LEVEL` | `INFO` | Logging level |
| `REQUEST_TIMEOUT` | `300` | Request timeout in seconds |
| `MAX_RETRIES` | `3` | Maximum retry attempts |
| `IMAGE_RESIZE_THRESHOLD` | `1024` | Max image dimension before resizing |

## Deployment

### Deploy to Render

1. Push your code to a Git repository
2. Create a new Web Service on Render
3. Connect your repository
4. Set the build command to: `pip install -r requirements.txt`
5. Set the start command to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (especially `HF_API_KEY`)
7. Deploy!

The `render.yaml` file is already configured for Render deployment.

### Deploy to Other Platforms

The application can be deployed to any platform that supports Python and FastAPI:

- **Heroku**: Use Procfile with `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Railway**: Similar to Render, configure start command
- **AWS Lambda**: Use AWS Lambda with FastAPI adapter
- **Docker**: Create a Dockerfile and deploy to any container platform

## Mobile Client Integration

The backend is designed to work seamlessly with the React Native mobile client. The client includes dedicated screens for all services including video generation. For detailed video integration instructions, see `VIDEO_INTEGRATION_GUIDE.md`.

## Performance Optimization

### Backend Optimization

- **Connection Pooling**: HTTP connections are reused for efficiency
- **Image Resizing**: Large images are automatically resized to reduce API call duration
- **Retry Logic**: Transient failures are automatically retried with exponential backoff
- **Async Operations**: All I/O operations use async/await for better concurrency

### Client Optimization

- **Image Caching**: Generated images are cached locally to avoid redundant API calls
- **Lazy Loading**: Images are loaded only when visible on screen
- **Compression**: Images are compressed before display to reduce memory usage
- **Background Processing**: Heavy operations are offloaded to background threads

## Monitoring and Logging

The application provides structured JSON logging for easy integration with monitoring systems:

```json
{
  "timestamp": "2025-12-22T10:30:00Z",
  "level": "INFO",
  "logger": "ai-platform",
  "message": "Image generated successfully",
  "model": "stabilityai/stable-diffusion-3-medium",
  "audio_size": 245120
}
```

## Troubleshooting

### HuggingFace API Key Issues

If you get authentication errors:
1. Verify your API key is correct: `echo $HF_API_KEY`
2. Check that the key has the necessary permissions
3. Ensure the key is not expired

### Model Not Found

If a model is not available:
1. Check that the model exists on HuggingFace Hub
2. Verify the model name is correct
3. The service will automatically try fallback models

### Timeout Errors

If requests timeout:
1. Increase `REQUEST_TIMEOUT` environment variable
2. Check your network connection
3. Verify HuggingFace API is not experiencing issues

### Out of Memory

If you get memory errors:
1. Reduce `IMAGE_RESIZE_THRESHOLD` to resize images more aggressively
2. Reduce `MAX_IMAGE_SIZE` to limit maximum image size
3. Deploy to a machine with more RAM

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black app/
```

### Linting

```bash
flake8 app/
```

### Type Checking

```bash
mypy app/
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [HuggingFace Hub Documentation](https://huggingface.co/docs/hub/index)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Render Deployment Guide](https://render.com/docs)
