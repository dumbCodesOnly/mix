# AI Platform Frontend

A modern, responsive web dashboard for interacting with the AI Platform Backend API. Built with React, TypeScript, and Tailwind CSS.

## Features

- **Image Generation** - Create stunning images from text descriptions using Stable Diffusion models
- **Image Editing** - Edit and enhance images with AI-powered inpainting (Coming Soon)
- **Text-to-Video** - Generate dynamic videos from text prompts (Coming Soon)
- **Image-to-Video** - Animate static images into captivating videos (Coming Soon)
- **Text-to-Speech** - Convert text to natural-sounding speech (Coming Soon)
- **Speech-to-Text** - Transcribe audio files with high accuracy (Coming Soon)
- **AI Chat** - Interact with state-of-the-art language models
- **Embeddings** - Generate vector embeddings for semantic search (Coming Soon)

## Tech Stack

- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS 4
- **UI Components**: shadcn/ui
- **Routing**: Wouter
- **HTTP Client**: Axios
- **State Management**: React Hooks

## Design Philosophy

The interface features a **premium, tech-forward aesthetic** with:

- **Typography**: Inter for UI elements, Space Grotesk for headings
- **Color Palette**: Deep purple/indigo gradients with cyan accents
- **Layout**: Sidebar navigation with modern grid-based content
- **Depth**: Subtle shadows, glassmorphism effects, and smooth animations

## Getting Started

### Prerequisites

- Node.js 18+ and pnpm
- AI Platform Backend running (see backend repository)

### Installation

1. Clone the repository:
\`\`\`bash
git clone <repository-url>
cd ai-platform-frontend
\`\`\`

2. Install dependencies:
\`\`\`bash
pnpm install
\`\`\`

3. Configure the backend URL:
   - The backend API URL is configured via environment variables
   - Update `VITE_API_URL` in the Manus dashboard settings
   - Default: `http://localhost:8000`

4. Start the development server:
\`\`\`bash
pnpm dev
\`\`\`

The application will be available at `http://localhost:3000`

## Project Structure

\`\`\`
client/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable UI components
│   │   ├── ui/         # shadcn/ui components
│   │   ├── DashboardLayout.tsx
│   │   └── ErrorBoundary.tsx
│   ├── contexts/        # React contexts
│   │   └── ThemeContext.tsx
│   ├── lib/            # Utility functions
│   │   ├── api.ts      # API client
│   │   └── utils.ts    # Helper functions
│   ├── pages/          # Page components
│   │   ├── Home.tsx
│   │   ├── ImageGeneration.tsx
│   │   ├── Chat.tsx
│   │   └── ...
│   ├── App.tsx         # Main app component with routing
│   ├── main.tsx        # Entry point
│   └── index.css       # Global styles and theme
\`\`\`

## Available Features

### ✅ Implemented

1. **Home Page** - Feature overview and navigation
2. **Image Generation** - Full implementation with model selection, parameter controls, and image preview
3. **AI Chat** - Multi-turn conversations with language models

### 🚧 Coming Soon

4. **Image Editing** - Upload and edit images with inpainting
5. **Text-to-Video** - Generate videos from text descriptions
6. **Image-to-Video** - Animate static images
7. **Text-to-Speech** - Convert text to audio
8. **Speech-to-Text** - Transcribe audio files
9. **Embeddings** - Generate text embeddings

## API Integration

The frontend communicates with the backend via the `apiClient` service located in `client/src/lib/api.ts`.

### Example Usage

\`\`\`typescript
import { apiClient } from '@/lib/api';

// Generate an image
const blob = await apiClient.generateImage({
  prompt: 'A serene landscape with mountains',
  width: 512,
  height: 512,
});

// Chat with LLM
const response = await apiClient.generateText({
  messages: [
    { role: 'user', content: 'Hello!' }
  ],
});
\`\`\`

## Configuration

### Backend URL

The backend API URL is configured via the `VITE_API_URL` environment variable. Update this in the Manus dashboard settings to point to your backend deployment.

### Theme

The application supports light and dark themes. The theme is configured in `client/src/App.tsx`:

\`\`\`typescript
<ThemeProvider defaultTheme="light">
  {/* App content */}
</ThemeProvider>
\`\`\`

To enable theme switching, uncomment the `switchable` prop:

\`\`\`typescript
<ThemeProvider defaultTheme="light" switchable>
  {/* App content */}
</ThemeProvider>
\`\`\`

## Development

### Adding New Features

1. Create a new page component in `client/src/pages/`
2. Add the route in `client/src/App.tsx`
3. Update the navigation in `client/src/components/DashboardLayout.tsx`
4. Implement the API integration in `client/src/lib/api.ts`

### Styling Guidelines

- Use Tailwind utility classes for styling
- Leverage shadcn/ui components for consistent UI
- Follow the existing color palette (purple/indigo with cyan accents)
- Use the Space Grotesk font for headings and Inter for body text

## Deployment

### Build for Production

\`\`\`bash
pnpm build
\`\`\`

The built files will be in the `dist/` directory.

### Deploy

The application can be deployed to any static hosting service:

- **Manus** (Recommended) - Click the Publish button in the dashboard
- **Vercel** - Connect your repository and deploy
- **Netlify** - Drag and drop the `dist/` folder
- **Render** - Create a static site and connect your repository

## Troubleshooting

### Backend Connection Issues

1. Verify the backend is running and accessible
2. Check the `VITE_API_URL` environment variable
3. Ensure CORS is properly configured in the backend
4. Check browser console for network errors

### Build Errors

1. Clear node_modules and reinstall: `rm -rf node_modules && pnpm install`
2. Clear build cache: `rm -rf dist`
3. Check for TypeScript errors: `pnpm check`

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

## Related Projects

- [AI Platform Backend](../README.md) - FastAPI backend service
- [Mobile Client](../mobile_client/README.md) - React Native mobile app

---

Built with ❤️ using React, TypeScript, and Tailwind CSS
