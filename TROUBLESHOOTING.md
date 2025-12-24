# AI Platform - Troubleshooting Guide

This guide provides solutions for common issues encountered when using the AI Platform backend and frontend.

## Table of Contents

1. [Backend Issues](#backend-issues)
2. [Frontend Issues](#frontend-issues)
3. [API Integration Issues](#api-integration-issues)
4. [Performance Issues](#performance-issues)
5. [Deployment Issues](#deployment-issues)

## Backend Issues

### HuggingFace API Errors

#### Error: "410 Client Error: Gone for url: https://api-inference.huggingface.co"

**Cause**: The backend is using the deprecated HuggingFace API endpoint.

**Solution**:
1. Update your backend to the latest version
2. The new version automatically uses `https://router.huggingface.co`
3. Redeploy the backend on Render

**Verification**:
```bash
curl https://your-backend.onrender.com/health
```

#### Error: "401 Unauthorized" or "Invalid API Key"

**Cause**: HuggingFace API key is invalid, expired, or not set.

**Solution**:
1. Verify your HuggingFace API key at https://huggingface.co/settings/tokens
2. Check that the key has API access enabled
3. Update the `HF_API_KEY` environment variable in Render
4. Redeploy the backend

**Verification**:
```bash
# Check if API key is set (backend logs)
docker logs <container_id> | grep "HuggingFace client initialized"
```

#### Error: "Model not found" or "404 Not Found"

**Cause**: The specified model doesn't exist or isn't accessible.

**Solution**:
1. Verify the model ID is correct at https://huggingface.co/models
2. Ensure the model is public or your API key has access
3. Check that the model supports the requested task (e.g., text-to-image)
4. Try using a default model instead

**Example**: Instead of a custom model, use:
```json
{
  "prompt": "A beautiful sunset",
  "model": "stabilityai/stable-diffusion-3-medium"
}
```

#### Error: "Request timed out" or "504 Gateway Timeout"

**Cause**: HuggingFace API is slow or the request is too complex.

**Solution**:
1. Increase `REQUEST_TIMEOUT` in backend environment variables (try 180 seconds)
2. Try a simpler prompt or smaller resolution
3. Try a faster model (e.g., FLUX instead of Stable Diffusion)
4. Retry the request after a few seconds

**For Video Generation**:
- Reduce `duration` (try 3 seconds instead of 6)
- Reduce `fps` (try 4 instead of 8)
- Reduce `num_inference_steps` (try 25 instead of 50)

### Backend Service Issues

#### Error: "Backend service is not running"

**Cause**: The backend service crashed or failed to start.

**Solution**:
1. Check Render dashboard for service status
2. View logs to identify the error
3. Check environment variables are set correctly
4. Redeploy the service

**Check Logs**:
```bash
# In Render dashboard, click "Logs" tab
# Look for error messages like:
# - "ModuleNotFoundError"
# - "ValueError"
# - "Connection refused"
```

#### Error: "Port 8000 is already in use"

**Cause**: Another process is using port 8000.

**Solution** (Local Development):
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
python -m uvicorn app.main:app --port 8001
```

#### Error: "ModuleNotFoundError: No module named 'huggingface_hub'"

**Cause**: Dependencies not installed.

**Solution**:
1. Ensure `requirements.txt` is in the `backend/` directory
2. Check that all dependencies are listed
3. Redeploy on Render (it will reinstall dependencies)

**Local Development**:
```bash
cd backend
pip install -r requirements.txt
```

### CORS Issues

#### Error: "Access to XMLHttpRequest has been blocked by CORS policy"

**Cause**: Backend CORS settings don't allow frontend domain.

**Solution**:
1. Go to Render backend settings
2. Update `ALLOWED_ORIGINS` environment variable
3. Include your frontend URL: `https://your-frontend.onrender.com`
4. Redeploy the backend

**Example**:
```
ALLOWED_ORIGINS=https://ai-platform-frontend.onrender.com,http://localhost:3000
```

## Frontend Issues

### Build Errors

#### Error: "No package.json found in /opt/render/project/src"

**Cause**: Render can't find the frontend package.json.

**Solution**:
1. In Render settings, set `Root Directory` to `frontend`
2. Verify `package.json` exists at `frontend/package.json`
3. Redeploy

**Verify Locally**:
```bash
ls -la frontend/package.json
```

#### Error: "pnpm: command not found"

**Cause**: pnpm is not installed in the build environment.

**Solution**:
1. Change build command to use npm instead:
   ```
   npm install && npm run build
   ```
2. Or ensure pnpm is available (Render usually has it pre-installed)

#### Error: "Build failed" (generic)

**Solution**:
1. Check Render build logs for specific error
2. Look for missing dependencies
3. Check for TypeScript errors
4. Verify environment variables are set

**Common Causes**:
- Missing environment variable `VITE_API_URL`
- Outdated dependencies
- TypeScript compilation errors

### Runtime Errors

#### Error: "Blank page" or "Cannot read properties of undefined"

**Cause**: Frontend can't connect to backend or JavaScript error.

**Solution**:
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab to see if API requests are failing
4. Verify `VITE_API_URL` is correct

**Debug Steps**:
```javascript
// In browser console:
console.log(import.meta.env.VITE_API_URL)
// Should show your backend URL
```

#### Error: "Failed to fetch" or "Network error"

**Cause**: Frontend can't reach backend.

**Solution**:
1. Verify backend URL is correct in `VITE_API_URL`
2. Check that backend is running: `curl https://your-backend.onrender.com/health`
3. Check browser console for CORS errors
4. Verify firewall isn't blocking requests

#### Error: "Image generation returns 500 error"

**Cause**: Backend error during image generation.

**Solution**:
1. Check backend logs for the specific error
2. Verify HuggingFace API key is valid
3. Try with a simpler prompt
4. Try with a different model

**Example Simple Prompt**:
```json
{
  "prompt": "A cat"
}
```

### Styling Issues

#### Error: "Styles not loading" or "Page looks broken"

**Cause**: CSS files not loaded or Tailwind not compiled.

**Solution**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+Shift+R)
3. Check that `index.css` is imported in `main.tsx`
4. Verify Tailwind is configured in `tailwind.config.ts`

#### Error: "Dark mode not working"

**Cause**: Theme context not initialized.

**Solution**:
1. Check that `ThemeProvider` wraps the app in `App.tsx`
2. Verify theme context is properly exported
3. Check browser localStorage for theme preference

## API Integration Issues

### Image Generation

#### Error: "Image generation takes too long"

**Cause**: Model is slow or HuggingFace is overloaded.

**Solution**:
1. Try a faster model: `stabilityai/stable-diffusion-2-1` instead of `3-medium`
2. Reduce resolution: 512x512 instead of 1024x1024
3. Reduce inference steps: 30 instead of 50
4. Try again during off-peak hours

#### Error: "Generated image is low quality"

**Cause**: Model or parameters not optimal.

**Solution**:
1. Improve the prompt (be more descriptive)
2. Try a different model
3. Increase `num_inference_steps` (up to 100)
4. Increase `guidance_scale` (up to 15)

### Chat / LLM

#### Error: "Chat response is empty or incomplete"

**Cause**: Model didn't generate output or timed out.

**Solution**:
1. Increase `max_tokens` parameter
2. Try a different model
3. Simplify the prompt
4. Check backend logs for errors

#### Error: "Chat takes too long to respond"

**Cause**: Model is large or overloaded.

**Solution**:
1. Try a smaller/faster model
2. Reduce `max_tokens`
3. Reduce `num_inference_steps` if applicable
4. Check HuggingFace service status

### Text-to-Speech

#### Error: "Audio file is corrupted or won't play"

**Cause**: Audio encoding issue.

**Solution**:
1. Check that audio format is WAV (default)
2. Try a different browser
3. Try downloading the file and playing with a media player
4. Check backend logs for encoding errors

#### Error: "Speech synthesis is very slow"

**Cause**: Model is loading or overloaded.

**Solution**:
1. Try a different TTS model
2. Reduce text length
3. Retry after a few seconds

### Speech-to-Text

#### Error: "Transcription is inaccurate"

**Cause**: Audio quality or model limitations.

**Solution**:
1. Ensure audio quality is good (clear speech, minimal background noise)
2. Try a different STT model (e.g., `openai/whisper-large`)
3. Ensure audio format is supported (WAV, MP3, etc.)

#### Error: "STT request fails with 'invalid audio'"

**Cause**: Audio format not supported.

**Solution**:
1. Convert audio to WAV format
2. Ensure audio is mono or stereo
3. Check audio sample rate (typically 16000 Hz)
4. Verify file size is reasonable (< 100MB)

### Video Generation

#### Error: "Video generation fails with timeout"

**Cause**: Video generation is very slow.

**Solution**:
1. Reduce video duration (try 3 seconds)
2. Reduce FPS (try 4)
3. Reduce inference steps (try 25)
4. Increase `REQUEST_TIMEOUT` to 300+ seconds
5. Note: Video generation can take 5-10 minutes

#### Error: "Generated video won't play"

**Cause**: Video format or encoding issue.

**Solution**:
1. Try a different video player
2. Check backend logs for encoding errors
3. Verify video file size (should be several MB)
4. Try downloading and playing locally

### Text Embeddings

#### Error: "Embedding dimension mismatch"

**Cause**: Different models produce different embedding sizes.

**Solution**:
1. Ensure you're using the same model for all embeddings
2. Check model documentation for embedding dimension
3. Update your vector database schema if needed

## Performance Issues

### Slow Image Generation

**Typical Times**:
- Stable Diffusion 2.1: 30-60 seconds
- Stable Diffusion 3: 60-120 seconds
- FLUX: 30-90 seconds

**Optimization**:
1. Use a faster model
2. Reduce resolution
3. Reduce inference steps
4. Use smaller batch sizes

### Slow Chat Responses

**Typical Times**:
- Small models (7B): 5-15 seconds
- Large models (13B+): 30+ seconds

**Optimization**:
1. Use a smaller model
2. Reduce `max_tokens`
3. Simplify prompts

### Slow Video Generation

**Typical Times**:
- 3 seconds @ 4 FPS: 2-3 minutes
- 6 seconds @ 8 FPS: 5-10 minutes

**Optimization**:
1. Reduce duration
2. Reduce FPS
3. Reduce inference steps
4. Use a faster model (if available)

## Deployment Issues

### Backend Won't Deploy

#### Error: "Dockerfile not found"

**Solution**:
1. Verify `Root Directory` is set to `backend`
2. Check that `backend/Dockerfile` exists
3. Redeploy

#### Error: "Build failed"

**Solution**:
1. Check Render build logs
2. Look for specific error messages
3. Verify all dependencies in `requirements.txt`
4. Test build locally with Docker

**Local Docker Build**:
```bash
cd backend
docker build -t ai-platform-backend .
```

### Frontend Won't Deploy

#### Error: "Build command failed"

**Solution**:
1. Check Render build logs
2. Verify `Root Directory` is `frontend`
3. Check that all environment variables are set
4. Test build locally

**Local Build Test**:
```bash
cd frontend
pnpm install
pnpm build
```

### Services Won't Connect

#### Error: "Backend URL is incorrect"

**Solution**:
1. Verify backend URL in frontend environment variables
2. Test backend URL in browser
3. Check that backend is running
4. Verify CORS settings

**Test Backend**:
```bash
curl https://your-backend.onrender.com/health
```

## Getting Help

If you're still experiencing issues:

1. **Check Logs**: Review backend and frontend logs in Render
2. **Test Locally**: Reproduce the issue locally for easier debugging
3. **Check Status**: Verify HuggingFace service status at https://status.huggingface.co
4. **Review Documentation**: Check README and API docs
5. **Contact Support**: Open an issue on GitHub or contact the development team

## Common Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `410 Client Error: Gone` | Deprecated API endpoint | Update backend to latest version |
| `401 Unauthorized` | Invalid API key | Check HuggingFace API key |
| `404 Not Found` | Model not found | Verify model ID is correct |
| `504 Gateway Timeout` | Request too slow | Increase timeout or simplify request |
| `CORS error` | Backend doesn't allow frontend | Update ALLOWED_ORIGINS |
| `ModuleNotFoundError` | Missing dependency | Run pip install -r requirements.txt |
| `No package.json found` | Wrong root directory | Set Root Directory to `frontend` |
| `Blank page` | Frontend can't connect | Check VITE_API_URL |

## Performance Benchmarks

### Expected Response Times

| Feature | Model | Time |
|---------|-------|------|
| Image Generation | Stable Diffusion 3 | 60-120s |
| Image Generation | FLUX | 30-90s |
| Chat Response | Mistral 7B | 5-15s |
| Chat Response | Larger Models | 30+s |
| Text-to-Speech | Default | 5-10s |
| Speech-to-Text | Whisper Base | 10-30s |
| Embeddings | All-MiniLM | 1-2s |
| Video (3s @ 4fps) | Default | 2-3 min |
| Video (6s @ 8fps) | Default | 5-10 min |

---

**Last Updated**: December 24, 2025
**Version**: 1.0
**Author**: AI Platform Team
