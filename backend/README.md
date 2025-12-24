# AI Platform Backend

A production-ready FastAPI backend that provides unified access to multiple HuggingFace AI models through a comprehensive REST API.

## Overview

The AI Platform Backend is a robust, scalable service that abstracts the complexity of interacting with various HuggingFace models. It provides a single, unified interface for:

- **Image Generation** - Text-to-image synthesis using Stable Diffusion and FLUX models
- **Image Editing** - Inpainting and image-to-image transformations
- **Video Generation** - Text-to-video and image-to-video synthesis
- **Text-to-Speech** - Natural language audio synthesis
- **Speech-to-Text** - Audio transcription using Whisper
- **Large Language Models** - Multi-turn conversational AI
- **Text Embeddings** - Semantic vector representations

## Architecture

The backend follows a layered architecture with clear separation of concerns:

```
API Routes (FastAPI)
    ↓
Service Layer (Business Logic)
    ↓
HuggingFace Client (API Abstraction)
    ↓
HuggingFace Inference API (router.huggingface.co)
```

### Key Components

**Routers** - Handle HTTP requests and responses for each feature domain:
- `image_router.py` - Image generation and editing endpoints
- `llm_router.py` - Language model chat endpoints
- `tts_router.py` - Text-to-speech endpoints
- `stt_router.py` - Speech-to-text endpoints
- `video_router.py` - Video generation endpoints
- `embedding_router.py` - Text embedding endpoints
- `health_router.py` - Health check endpoints

**Services** - Implement business logic and coordinate with external APIs:
- `image_service.py` - Image processing and generation
- `llm_service.py` - Language model interactions
- `tts_service.py` - Text-to-speech synthesis
- `stt_service.py` - Speech-to-text transcription
- `video_service.py` - Video generation
- `embedding_service.py` - Text embedding generation
- `hf_client.py` - Centralized HuggingFace API client

**Utilities** - Cross-cutting concerns:
- `config.py` - Configuration management
- `exceptions.py` - Custom exception definitions
- `logging.py` - Structured logging
- `retry.py` - Retry logic with exponential backoff
- `validation.py` - Request/response validation

## Installation

### Prerequisites

- Python 3.11+
- HuggingFace API key (get one at https://huggingface.co/settings/tokens)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/dumbCodesOnly/mix.git
cd mix/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export HF_API_KEY=your_huggingface_api_key
export ALLOWED_ORIGINS=http://localhost:3000

# Run the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `HF_API_KEY` | HuggingFace API authentication token | - | Yes |
| `HOST` | Server host address | `0.0.0.0` | No |
| `PORT` | Server port number | `8000` | No |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | `http://localhost:3000` | No |
| `REQUEST_TIMEOUT` | API request timeout in seconds | `120` | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` | No |

### Model Configuration

Default models are configured in `app/utils/config.py`:

```python
DEFAULT_IMAGE_MODEL = "stabilityai/stable-diffusion-3-medium"
DEFAULT_IMAGE_EDIT_MODEL = "runwayml/stable-diffusion-inpainting"
DEFAULT_TTS_MODEL = "espnet/kan-bayashi_ljspeech_vits"
DEFAULT_STT_MODEL = "openai/whisper-base"
DEFAULT_LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_TEXT_TO_VIDEO_MODEL = "damo-vilab/text-to-video-ms-1.7b"
DEFAULT_IMAGE_TO_VIDEO_MODEL = "damo-vilab/image-to-video-ms-1.7b"
```

You can override these by passing `model` parameter in API requests.

## API Endpoints

### Image Generation

**POST** `/api/image`

Generate images from text prompts.

```bash
curl -X POST http://localhost:8000/api/image \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A serene landscape with mountains and a lake",
    "model": "stabilityai/stable-diffusion-3-medium",
    "height": 512,
    "width": 512,
    "num_inference_steps": 50,
    "guidance_scale": 7.5
  }'
```

**Response:**
```json
{
  "image": "base64_encoded_image_data",
  "model": "stabilityai/stable-diffusion-3-medium",
  "generation_time": 12.5,
  "size": 245632
}
```

### Image Editing

**POST** `/api/edit-image`

Edit images using inpainting with a mask.

```bash
curl -X POST http://localhost:8000/api/edit-image \
  -F "image=@original.png" \
  -F "mask=@mask.png" \
  -F "prompt=A red car" \
  -F "model=runwayml/stable-diffusion-inpainting"
```

### Chat / LLM

**POST** `/api/llm`

Multi-turn conversations with language models.

```bash
curl -X POST http://localhost:8000/api/llm \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is machine learning?"}
    ],
    "model": "mistralai/Mistral-7B-Instruct-v0.1",
    "max_tokens": 256,
    "temperature": 0.7
  }'
```

### Text-to-Speech

**POST** `/api/tts`

Convert text to audio.

```bash
curl -X POST http://localhost:8000/api/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, this is a test of the text to speech system.",
    "model": "espnet/kan-bayashi_ljspeech_vits"
  }' \
  -o output.wav
```

### Speech-to-Text

**POST** `/api/stt`

Transcribe audio to text.

```bash
curl -X POST http://localhost:8000/api/stt \
  -F "audio=@recording.wav" \
  -F "model=openai/whisper-base"
```

### Text Embeddings

**POST** `/api/embedding`

Generate semantic embeddings for text.

```bash
curl -X POST http://localhost:8000/api/embedding \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The quick brown fox jumps over the lazy dog",
    "model": "sentence-transformers/all-MiniLM-L6-v2"
  }'
```

### Video Generation

**POST** `/api/video/text-to-video`

Generate videos from text prompts.

```bash
curl -X POST http://localhost:8000/api/video/text-to-video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cat playing with a ball",
    "model": "damo-vilab/text-to-video-ms-1.7b",
    "duration": 6,
    "fps": 8
  }'
```

**POST** `/api/video/image-to-video`

Generate videos from images.

```bash
curl -X POST http://localhost:8000/api/video/image-to-video \
  -F "image=@input.png" \
  -F "prompt=The person is waving" \
  -F "model=damo-vilab/image-to-video-ms-1.7b"
```

### Health Check

**GET** `/health`

Check backend health status.

```bash
curl http://localhost:8000/health
```

## Error Handling

The backend implements comprehensive error handling with meaningful error messages:

```json
{
  "detail": "Failed to generate image: 410 Client Error: Gone",
  "error_code": "HUGGINGFACE_API_ERROR",
  "status_code": 500
}
```

Common error codes:

| Code | Meaning | Solution |
|------|---------|----------|
| `INVALID_API_KEY` | HuggingFace API key is invalid | Check your `HF_API_KEY` environment variable |
| `MODEL_NOT_FOUND` | Model not found on HuggingFace | Verify model ID is correct |
| `TIMEOUT_ERROR` | Request timed out | Increase `REQUEST_TIMEOUT` or try again |
| `VALIDATION_ERROR` | Invalid request parameters | Check request format and parameters |
| `HUGGINGFACE_API_ERROR` | HuggingFace API error | Check HuggingFace service status |

## Retry Logic

The backend implements automatic retry with exponential backoff for transient failures:

- **Max Retries**: 4 attempts
- **Initial Delay**: 1 second
- **Backoff Factor**: 2x (1s → 2s → 4s → 8s)
- **Max Delay**: 60 seconds

This ensures reliability when dealing with temporary network issues or API rate limiting.

## Deployment

### Docker

Build and run the backend in a Docker container:

```bash
# Build the image
docker build -t ai-platform-backend .

# Run the container
docker run -p 8000:8000 \
  -e HF_API_KEY=your_api_key \
  -e ALLOWED_ORIGINS=https://your-frontend.com \
  ai-platform-backend
```

### Render Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed Render deployment instructions.

### Environment-Specific Configuration

**Development:**
```bash
export LOG_LEVEL=DEBUG
export ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Production:**
```bash
export LOG_LEVEL=INFO
export ALLOWED_ORIGINS=https://your-frontend-domain.com
export REQUEST_TIMEOUT=60
```

## HuggingFace API Endpoint

**Important**: The backend uses the new HuggingFace router endpoint (`https://router.huggingface.co`) instead of the deprecated `api-inference.huggingface.co` endpoint. This is automatically configured in the `HuggingFaceClient` class.

If you encounter 410 errors, ensure your backend is running the latest version with the updated endpoint configuration.

## Performance Optimization

### Image Generation

- **Batch Processing**: Not supported by HuggingFace Inference API
- **Model Selection**: Smaller models (e.g., FLUX) are faster but lower quality
- **Resolution**: Lower resolutions (256x256) generate faster than higher ones (1024x1024)

### Video Generation

- **Duration**: Longer videos take exponentially more time
- **FPS**: Higher FPS values increase generation time
- **Model**: Different models have different speed/quality tradeoffs

### Caching

The backend does not implement response caching by design, as AI model outputs are non-deterministic. Implement caching at the frontend or proxy level if needed.

## Monitoring

### Health Checks

The `/health` endpoint provides real-time service status:

```bash
curl http://localhost:8000/health
```

Response indicates whether the service is operational and can reach HuggingFace APIs.

### Logging

Structured logging is enabled by default. Logs include:
- Request/response details
- Model inference times
- Error stack traces
- API rate limit information

View logs:
```bash
# Docker
docker logs <container_id>

# Local
tail -f logs/app.log
```

## Troubleshooting

### Common Issues

**Issue**: "HuggingFace API key is required"
- **Solution**: Set the `HF_API_KEY` environment variable

**Issue**: "410 Client Error: Gone for url: https://api-inference.huggingface.co"
- **Solution**: This error indicates you're using an outdated backend version. Update to the latest version that uses `router.huggingface.co`

**Issue**: "Model not found"
- **Solution**: Verify the model ID exists on HuggingFace Hub and is accessible with your API key

**Issue**: "Request timed out"
- **Solution**: Increase `REQUEST_TIMEOUT` environment variable or try a simpler model

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for more detailed troubleshooting guides.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The project uses:
- **Formatter**: Black
- **Linter**: Pylint
- **Type Checker**: Mypy

Format code:
```bash
black app/
```

### Adding New Features

1. Create a new service in `app/services/`
2. Create a new router in `app/routers/`
3. Add routes to `app/main.py`
4. Update documentation

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:

1. Check the [Troubleshooting Guide](./TROUBLESHOOTING.md)
2. Review the [API Documentation](http://localhost:8000/docs)
3. Open an issue on GitHub
4. Contact the development team

## References

- [HuggingFace Hub](https://huggingface.co)
- [HuggingFace Inference API Documentation](https://huggingface.co/docs/hub/inference-api)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pydantic Documentation](https://docs.pydantic.dev)
