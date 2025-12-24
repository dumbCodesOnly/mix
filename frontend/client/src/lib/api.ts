import axios, { AxiosInstance, AxiosError } from 'axios';

// Backend API base URL - update this to point to your deployed backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ImageGenerationRequest {
  prompt: string;
  model?: string;
  negative_prompt?: string;
  height?: number;
  width?: number;
  num_inference_steps?: number;
  guidance_scale?: number;
}

export interface ImageEditRequest {
  image: string; // base64
  prompt: string;
  mask?: string; // base64
  model?: string;
  negative_prompt?: string;
  strength?: number;
  num_inference_steps?: number;
  guidance_scale?: number;
}

export interface TTSRequest {
  text: string;
  model?: string;
  speaker_id?: number;
  speed?: number;
}

export interface STTResponse {
  text: string;
  language: string;
  confidence: number;
  model: string;
}

export interface LLMRequest {
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>;
  model?: string;
  max_tokens?: number;
  temperature?: number;
  top_p?: number;
  top_k?: number;
}

export interface LLMResponse {
  response: string;
  model: string;
  tokens_used: number;
  stop_reason: string;
}

export interface EmbeddingRequest {
  text: string;
  model?: string;
}

export interface EmbeddingResponse {
  embedding: number[];
  dimension: number;
  model: string;
  tokens_used: number;
}

export interface VideoTextToVideoRequest {
  prompt: string;
  model?: string;
  negative_prompt?: string;
  duration?: number;
  fps?: number;
  num_inference_steps?: number;
}

export interface VideoImageToVideoRequest {
  prompt?: string;
  duration?: number;
  fps?: number;
  num_inference_steps?: number;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
}

class APIClient {
  private client: AxiosInstance;

  constructor(baseURL: string = API_BASE_URL) {
    this.client = axios.create({
      baseURL,
      timeout: 300000, // 5 minutes for long-running AI operations
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response) {
          // Server responded with error
          console.error('API Error:', error.response.data);
        } else if (error.request) {
          // Request made but no response
          console.error('Network Error:', error.message);
        }
        throw error;
      }
    );
  }

  async healthCheck(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>('/health');
    return response.data;
  }

  async generateImage(request: ImageGenerationRequest): Promise<Blob> {
    const response = await this.client.post('/api/image', request, {
      responseType: 'blob',
    });
    return response.data;
  }

  async editImage(request: ImageEditRequest): Promise<Blob> {
    const response = await this.client.post('/api/edit-image', request, {
      responseType: 'blob',
    });
    return response.data;
  }

  async textToSpeech(request: TTSRequest): Promise<Blob> {
    const response = await this.client.post('/api/tts', request, {
      responseType: 'blob',
    });
    return response.data;
  }

  async speechToText(audioFile: File, language?: string, model?: string): Promise<STTResponse> {
    const formData = new FormData();
    formData.append('audio', audioFile);
    if (language) formData.append('language', language);
    if (model) formData.append('model', model);

    const response = await this.client.post<STTResponse>('/api/stt', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async generateText(request: LLMRequest): Promise<LLMResponse> {
    const response = await this.client.post<LLMResponse>('/api/llm', request);
    return response.data;
  }

  async generateEmbedding(request: EmbeddingRequest): Promise<EmbeddingResponse> {
    const response = await this.client.post<EmbeddingResponse>('/api/embedding', request);
    return response.data;
  }

  async generateTextToVideo(request: VideoTextToVideoRequest): Promise<Blob> {
    const response = await this.client.post('/api/video/text-to-video', request, {
      responseType: 'blob',
    });
    return response.data;
  }

  async generateImageToVideo(imageFile: File, request: VideoImageToVideoRequest): Promise<Blob> {
    const formData = new FormData();
    formData.append('image', imageFile);
    if (request.prompt) formData.append('prompt', request.prompt);
    if (request.duration) formData.append('duration', request.duration.toString());
    if (request.fps) formData.append('fps', request.fps.toString());
    if (request.num_inference_steps) formData.append('num_inference_steps', request.num_inference_steps.toString());

    const response = await this.client.post('/api/video/image-to-video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
    });
    return response.data;
  }
}

// Singleton instance
export const apiClient = new APIClient();

// Helper functions
export const downloadBlob = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

export const blobToBase64 = (blob: Blob): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64 = reader.result as string;
      // Remove data URL prefix
      const base64Data = base64.split(',')[1];
      resolve(base64Data);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
};

export const fileToBase64 = (file: File): Promise<string> => {
  return blobToBase64(file);
};
