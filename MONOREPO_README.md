# AI Platform - Monorepo

This repository contains the complete AI Platform application with both backend and frontend code.

## Repository Structure

```
mix/
├── backend/                 # FastAPI backend service
│   ├── app/                # Application code
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Docker configuration
│   └── docker-compose.yml  # Docker Compose setup
├── frontend/               # React frontend application
│   ├── client/            # React application
│   ├── server/            # Express server for production
│   ├── package.json       # Node dependencies
│   ├── render.yaml        # Render deployment config
│   └── DEPLOYMENT.md      # Frontend deployment guide
├── mobile_client/          # React Native mobile app
├── README.md              # Backend documentation
├── ARCHITECTURE.md        # System architecture
├── PROJECT_SUMMARY.md     # Project overview
└── plan.md               # Development plan
```

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
pnpm install
pnpm dev
```

Frontend will be available at: `http://localhost:3000`

## Deployment

### Backend Deployment (Render)

1. Deploy backend as a Web Service on Render
2. Set environment variables (HF_API_KEY, ALLOWED_ORIGINS, etc.)
3. Backend URL will be: `https://your-backend.onrender.com`

See `backend/DEPLOYMENT.md` for detailed instructions.

### Frontend Deployment (Render)

1. Deploy frontend as a Static Site on Render
2. Build command: `cd frontend && pnpm install && pnpm build`
3. Publish directory: `frontend/dist/public`
4. Set `VITE_API_URL` to your backend URL

See `frontend/DEPLOYMENT.md` for detailed instructions.

## Features

### Backend (FastAPI)
- ✅ Image Generation (Stable Diffusion, FLUX)
- ✅ Image Editing (Inpainting)
- ✅ Text-to-Speech
- ✅ Speech-to-Text (Whisper)
- ✅ Large Language Models (Chat)
- ✅ Text Embeddings
- ✅ Video Generation (Text-to-Video, Image-to-Video)

### Frontend (React)
- ✅ Image Generation Interface
- ✅ AI Chat Interface
- ✅ Modern Dashboard UI
- 🚧 Image Editing (Coming Soon)
- 🚧 Video Generation (Coming Soon)
- 🚧 Audio Features (Coming Soon)

## Environment Configuration

### Backend (.env)

```env
HF_API_KEY=your_huggingface_api_key
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.onrender.com
```

### Frontend (Render Environment Variables)

```
VITE_API_URL=http://localhost:8000  # Or your deployed backend URL
```

## Development

### Adding Features

1. **Backend**: Add new router in `backend/app/routers/`
2. **Frontend**: Add new page in `frontend/client/src/pages/`
3. **API Client**: Update `frontend/client/src/lib/api.ts`

### Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
pnpm test
```

## Documentation

- **Architecture**: See `ARCHITECTURE.md`
- **Backend API**: See `backend/README.md`
- **Frontend**: See `frontend/README.md`
- **Video Features**: See `VIDEO_SERVICE_ARCHITECTURE.md`
- **Deployment**: See `DEPLOYMENT.md` in each directory

## Support

For issues or questions:
1. Check the relevant README files
2. Review the ARCHITECTURE.md for system design
3. Check deployment guides for setup issues

## License

MIT License - See LICENSE file for details
