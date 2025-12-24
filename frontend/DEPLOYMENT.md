# Deployment Guide - AI Platform Frontend

This guide explains how to deploy the AI Platform frontend to Render.

## Prerequisites

- GitHub account with the repository pushed
- Render account (https://render.com)
- Backend API deployed and accessible

## Deployment Steps

### 1. Push to GitHub

First, ensure your code is pushed to GitHub:

```bash
git add .
git commit -m "Initial frontend deployment"
git push origin main
```

### 2. Connect to Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Static Site**
3. Connect your GitHub repository
4. Select the repository and branch (main)

### 3. Configure Build Settings

In the Render dashboard:

- **Name**: `ai-platform-frontend` (or your preferred name)
- **Root Directory**: Leave empty (or set to `/` if needed)
- **Build Command**: `pnpm install && pnpm build`
- **Publish Directory**: `dist/public`

### 4. Set Environment Variables

Add the following environment variable in Render:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | Your backend API URL (e.g., `https://your-backend.onrender.com`) |

**Important**: The backend URL must be accessible from the browser and have CORS configured to allow your frontend domain.

### 5. Deploy

Click **Create Static Site** to start the deployment. Render will:

1. Clone your repository
2. Install dependencies with `pnpm`
3. Build the project with `pnpm build`
4. Deploy the `dist/public` directory

### 6. Verify Deployment

Once deployed:

1. Visit your Render URL (e.g., `https://ai-platform-frontend.onrender.com`)
2. Test the Image Generation feature
3. Test the Chat feature
4. Check browser console for any errors

## Troubleshooting

### Build Fails

**Error**: `pnpm: command not found`
- **Solution**: Render should have pnpm pre-installed. If not, use `npm install && npm run build` instead.

### API Calls Fail

**Error**: `CORS error` or `Failed to fetch`
- **Solution**: 
  1. Verify `VITE_API_URL` is set correctly in Render environment variables
  2. Ensure backend has CORS configured to allow your frontend domain
  3. Check that backend is running and accessible

### Blank Page

**Error**: Page loads but shows nothing
- **Solution**:
  1. Check browser console (F12) for JavaScript errors
  2. Verify all assets loaded correctly
  3. Check that `dist/public` directory contains `index.html`

## Environment Variables

### VITE_API_URL

The base URL for the backend API. This is used by the frontend to make requests to:
- `/api/image` - Image generation
- `/api/edit-image` - Image editing
- `/api/tts` - Text-to-speech
- `/api/stt` - Speech-to-text
- `/api/llm` - Language model
- `/api/embedding` - Embeddings
- `/api/video/text-to-video` - Text-to-video
- `/api/video/image-to-video` - Image-to-video

**Example**: `https://ai-platform-backend.onrender.com`

## Custom Domain

To use a custom domain:

1. In Render dashboard, go to your site settings
2. Click **Custom Domain**
3. Add your domain and follow DNS configuration instructions

## Monitoring

Render provides logs and monitoring:

1. Click on your site in the dashboard
2. View **Logs** to see deployment and runtime logs
3. View **Metrics** to see traffic and performance

## Updates

To update the frontend:

1. Make changes locally
2. Commit and push to GitHub
3. Render will automatically redeploy on push (if auto-deploy is enabled)

To manually trigger a redeploy:
1. Go to your site in Render dashboard
2. Click **Manual Deploy** → **Deploy latest commit**

## Backend Configuration

Make sure your backend is configured to accept requests from your frontend domain:

```python
# In backend .env
ALLOWED_ORIGINS=https://ai-platform-frontend.onrender.com,http://localhost:3000
```

Or for development:
```python
ALLOWED_ORIGINS=*
```

## Performance Tips

1. **Enable Caching**: Render caches static assets automatically
2. **Optimize Images**: Use optimized image formats
3. **Code Splitting**: The build process automatically code-splits React components
4. **Lazy Loading**: Components are lazy-loaded for better performance

## Support

For issues with Render deployment, see:
- [Render Documentation](https://render.com/docs)
- [Render Support](https://render.com/support)

For issues with the frontend application, see:
- [Frontend README](./README.md)
- [Backend Documentation](../README.md)
