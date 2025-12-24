# AI Platform - Complete Deployment Guide

This guide provides step-by-step instructions for deploying the AI Platform (both backend and frontend) to production using Render.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Monitoring and Maintenance](#monitoring-and-maintenance)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting, ensure you have:

- **GitHub Account**: Repository access at https://github.com/dumbCodesOnly/mix
- **Render Account**: Create one at https://render.com
- **HuggingFace Account**: API key from https://huggingface.co/settings/tokens
- **Domain (Optional)**: For custom domain setup

## Backend Deployment

### Step 1: Prepare Backend Configuration

The backend is located in the `backend/` directory of the monorepo. Ensure the following files are in place:

- `backend/app/` - Application source code
- `backend/requirements.txt` - Python dependencies
- `backend/Dockerfile` - Container configuration

### Step 2: Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository (`dumbCodesOnly/mix`)
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `ai-platform-backend` |
| **Root Directory** | `backend` |
| **Runtime** | `Docker` |
| **Region** | Select closest to your users |
| **Plan** | Free (or paid for production) |

### Step 3: Configure Build Settings

In the Render dashboard:

1. **Build Command**: Leave as default (uses Dockerfile)
2. **Dockerfile Path**: `backend/Dockerfile`
3. **Docker Context**: `/backend`

### Step 4: Set Environment Variables

Add these environment variables in Render settings:

| Variable | Value | Notes |
|----------|-------|-------|
| `HF_API_KEY` | Your HuggingFace API key | Get from https://huggingface.co/settings/tokens |
| `ALLOWED_ORIGINS` | `https://your-frontend-url.onrender.com` | Update after frontend deployment |
| `LOG_LEVEL` | `INFO` | Use `DEBUG` for troubleshooting |
| `REQUEST_TIMEOUT` | `120` | Timeout for API requests in seconds |

### Step 5: Deploy Backend

1. Click **Create Web Service**
2. Render will automatically build and deploy your backend
3. Wait for deployment to complete (usually 3-5 minutes)
4. Note your backend URL (e.g., `https://ai-platform-backend.onrender.com`)

### Verify Backend Deployment

Test your backend with:

```bash
curl https://ai-platform-backend.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "AI Platform Backend"
}
```

## Frontend Deployment

### Step 1: Prepare Frontend Configuration

The frontend is located in the `frontend/` directory. Ensure:

- `frontend/client/` - React application
- `frontend/package.json` - Dependencies
- `frontend/render.yaml` - Render configuration

### Step 2: Create Render Static Site

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Static Site**
3. Connect your GitHub repository (`dumbCodesOnly/mix`)
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `ai-platform-frontend` |
| **Root Directory** | `frontend` |
| **Build Command** | `pnpm install && pnpm build` |
| **Publish Directory** | `dist/public` |
| **Region** | Same as backend |

### Step 3: Set Environment Variables

Add this environment variable:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | Your backend URL (e.g., `https://ai-platform-backend.onrender.com`) |

### Step 4: Deploy Frontend

1. Click **Create Static Site**
2. Render will build and deploy your frontend
3. Wait for deployment to complete (usually 2-3 minutes)
4. Note your frontend URL (e.g., `https://ai-platform-frontend.onrender.com`)

### Verify Frontend Deployment

1. Visit your frontend URL in a browser
2. You should see the AI Platform dashboard
3. Test the Image Generation feature to verify backend connectivity

## Post-Deployment Configuration

### Update Backend CORS Settings

Now that both services are deployed, update the backend's `ALLOWED_ORIGINS`:

1. Go to your backend service in Render
2. Click **Environment** in the left sidebar
3. Update `ALLOWED_ORIGINS` to include your frontend URL:
   ```
   https://ai-platform-frontend.onrender.com,http://localhost:3000
   ```
4. Click **Save**
5. Render will automatically redeploy with the new settings

### Configure Custom Domain (Optional)

To use a custom domain:

#### For Backend:
1. Go to backend service settings
2. Click **Custom Domain** in the left sidebar
3. Enter your domain (e.g., `api.yourcompany.com`)
4. Follow DNS configuration instructions
5. Update frontend's `VITE_API_URL` to use the custom domain

#### For Frontend:
1. Go to frontend service settings
2. Click **Custom Domain**
3. Enter your domain (e.g., `app.yourcompany.com`)
4. Follow DNS configuration instructions

### Enable Auto-Deployment

Both services are configured to automatically redeploy when you push to the `main` branch. To disable:

1. Go to service settings
2. Click **Deploys**
3. Toggle **Auto-deploy** off

## Monitoring and Maintenance

### View Logs

**Backend Logs:**
1. Go to backend service in Render
2. Click **Logs** in the left sidebar
3. View real-time logs

**Frontend Logs:**
1. Go to frontend service in Render
2. Click **Logs** in the left sidebar
3. View build and deployment logs

### Monitor Performance

**Backend Metrics:**
1. Go to backend service
2. Click **Metrics** to view:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

**Frontend Metrics:**
1. Go to frontend service
2. Click **Metrics** to view:
   - Build times
   - Deployment status
   - Traffic patterns

### Set Up Alerts (Paid Plan)

On paid Render plans, you can set up alerts for:
- Service failures
- High CPU/memory usage
- Deployment failures

### Backup and Recovery

**Backend Data:**
- The backend is stateless and doesn't store data
- All data is retrieved from HuggingFace APIs
- No backup needed

**Frontend Assets:**
- Automatically backed up by Render
- Redeploy from GitHub if needed

### Update Dependencies

To update dependencies:

1. Update `backend/requirements.txt` or `frontend/package.json`
2. Commit and push to GitHub
3. Services will automatically redeploy with new dependencies

## Troubleshooting

### Backend Won't Deploy

**Error**: "Dockerfile not found"
- **Solution**: Ensure `Root Directory` is set to `backend`

**Error**: "HuggingFace API key is required"
- **Solution**: Check that `HF_API_KEY` environment variable is set

**Error**: "410 Client Error: Gone for url: https://api-inference.huggingface.co"
- **Solution**: Update to latest backend version (uses `router.huggingface.co`)

### Frontend Won't Deploy

**Error**: "No package.json found"
- **Solution**: Ensure `Root Directory` is set to `frontend`

**Error**: "Build failed"
- **Solution**: Check build logs for specific errors, usually missing dependencies

### API Calls Fail

**Error**: "CORS error" or "Failed to fetch"
- **Solution**: 
  1. Verify `VITE_API_URL` is set correctly in frontend
  2. Check backend's `ALLOWED_ORIGINS` includes frontend URL
  3. Ensure backend is running (check health endpoint)

**Error**: "401 Unauthorized"
- **Solution**: Check that `HF_API_KEY` is valid and has API access

### Slow Performance

**Backend is slow:**
- Check HuggingFace service status
- Try a smaller/faster model
- Increase `REQUEST_TIMEOUT` if requests are timing out

**Frontend is slow:**
- Check network tab in browser DevTools
- Verify backend is responding quickly
- Clear browser cache

### Service Won't Stay Running

**Backend crashes after deployment:**
1. Check logs for error messages
2. Verify all environment variables are set
3. Ensure Docker image builds successfully locally

**Frontend shows blank page:**
1. Check browser console for errors
2. Verify `VITE_API_URL` is correct
3. Check that backend is accessible

## Maintenance Checklist

### Weekly

- [ ] Check service logs for errors
- [ ] Monitor performance metrics
- [ ] Verify both services are running

### Monthly

- [ ] Review and update dependencies
- [ ] Check HuggingFace API usage
- [ ] Verify custom domain DNS is working (if applicable)

### Quarterly

- [ ] Update to latest Python/Node versions
- [ ] Review and optimize performance
- [ ] Audit security settings

## Scaling Considerations

### Backend Scaling

For higher traffic, consider:

1. **Paid Plan**: Upgrade from free to paid Render plan
2. **Larger Instance**: Increase CPU/memory allocation
3. **Load Balancing**: Use Render's load balancing features
4. **Caching**: Implement response caching for common requests

### Frontend Scaling

The frontend is static and automatically scales with Render's CDN. No additional configuration needed.

## Security Best Practices

1. **Never commit secrets**: Use environment variables for API keys
2. **Rotate API keys**: Periodically update HuggingFace API key
3. **Enable HTTPS**: Render automatically provides SSL/TLS
4. **Restrict CORS**: Only allow your frontend domain in `ALLOWED_ORIGINS`
5. **Monitor logs**: Regularly check logs for suspicious activity

## Support and Resources

- **Render Documentation**: https://render.com/docs
- **HuggingFace Documentation**: https://huggingface.co/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **React Documentation**: https://react.dev

## Next Steps

After successful deployment:

1. **Test all features**: Image generation, chat, TTS, STT, video, embeddings
2. **Set up monitoring**: Configure alerts and metrics
3. **Plan scaling**: Estimate traffic and plan for growth
4. **Document changes**: Keep deployment notes for your team
5. **Set up CI/CD**: Consider adding automated tests to deployment pipeline

## Deployment Summary

| Component | Service | Status | URL |
|-----------|---------|--------|-----|
| Backend | Render Web Service | ✅ Deployed | `https://ai-platform-backend.onrender.com` |
| Frontend | Render Static Site | ✅ Deployed | `https://ai-platform-frontend.onrender.com` |
| Database | N/A | N/A | Stateless |
| Storage | HuggingFace | ✅ Connected | Via API |

---

**Last Updated**: December 24, 2025
**Version**: 1.0
**Author**: AI Platform Team
