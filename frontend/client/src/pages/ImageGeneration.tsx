import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { toast } from 'sonner';
import { Loader2, Download, Sparkles, Image as ImageIcon } from 'lucide-react';
import DashboardLayout from '@/components/DashboardLayout';
import { apiClient, downloadBlob } from '@/lib/api';

const models = [
  { value: 'stabilityai/stable-diffusion-3-medium', label: 'Stable Diffusion 3 Medium' },
  { value: 'black-forest-labs/FLUX.1-dev', label: 'FLUX.1 Dev' },
  { value: 'runwayml/stable-diffusion-v1-5', label: 'Stable Diffusion v1.5' },
];

export default function ImageGeneration() {
  const [prompt, setPrompt] = useState('');
  const [negativePrompt, setNegativePrompt] = useState('');
  const [model, setModel] = useState(models[0].value);
  const [width, setWidth] = useState(512);
  const [height, setHeight] = useState(512);
  const [steps, setSteps] = useState(50);
  const [guidanceScale, setGuidanceScale] = useState(7.5);
  const [loading, setLoading] = useState(false);
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error('Please enter a prompt');
      return;
    }

    setLoading(true);
    setGeneratedImage(null);

    try {
      const blob = await apiClient.generateImage({
        prompt,
        negative_prompt: negativePrompt || undefined,
        model,
        width,
        height,
        num_inference_steps: steps,
        guidance_scale: guidanceScale,
      });

      const url = URL.createObjectURL(blob);
      setGeneratedImage(url);
      toast.success('Image generated successfully!');
    } catch (error: any) {
      console.error('Generation error:', error);
      toast.error(error.response?.data?.message || 'Failed to generate image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (generatedImage) {
      fetch(generatedImage)
        .then(res => res.blob())
        .then(blob => downloadBlob(blob, `generated-${Date.now()}.png`));
      toast.success('Image downloaded!');
    }
  };

  return (
    <DashboardLayout>
      <div className="container py-8 max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500">
              <ImageIcon className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold">Image Generation</h1>
          </div>
          <p className="text-muted-foreground">
            Create stunning images from text descriptions using state-of-the-art AI models
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Controls */}
          <Card>
            <CardHeader>
              <CardTitle>Generation Settings</CardTitle>
              <CardDescription>Configure your image generation parameters</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Prompt */}
              <div className="space-y-2">
                <Label htmlFor="prompt">Prompt *</Label>
                <Textarea
                  id="prompt"
                  placeholder="A serene landscape with mountains and sunset..."
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  rows={4}
                  className="resize-none"
                />
              </div>

              {/* Negative Prompt */}
              <div className="space-y-2">
                <Label htmlFor="negative-prompt">Negative Prompt</Label>
                <Textarea
                  id="negative-prompt"
                  placeholder="blurry, low quality, distorted..."
                  value={negativePrompt}
                  onChange={(e) => setNegativePrompt(e.target.value)}
                  rows={2}
                  className="resize-none"
                />
              </div>

              {/* Model Selection */}
              <div className="space-y-2">
                <Label htmlFor="model">Model</Label>
                <Select value={model} onValueChange={setModel}>
                  <SelectTrigger id="model">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {models.map((m) => (
                      <SelectItem key={m.value} value={m.value}>
                        {m.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Dimensions */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="width">Width: {width}px</Label>
                  <Slider
                    id="width"
                    min={256}
                    max={1024}
                    step={64}
                    value={[width]}
                    onValueChange={([value]) => setWidth(value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="height">Height: {height}px</Label>
                  <Slider
                    id="height"
                    min={256}
                    max={1024}
                    step={64}
                    value={[height]}
                    onValueChange={([value]) => setHeight(value)}
                  />
                </div>
              </div>

              {/* Inference Steps */}
              <div className="space-y-2">
                <Label htmlFor="steps">Inference Steps: {steps}</Label>
                <Slider
                  id="steps"
                  min={10}
                  max={100}
                  step={5}
                  value={[steps]}
                  onValueChange={([value]) => setSteps(value)}
                />
                <p className="text-xs text-muted-foreground">Higher values = better quality but slower</p>
              </div>

              {/* Guidance Scale */}
              <div className="space-y-2">
                <Label htmlFor="guidance">Guidance Scale: {guidanceScale}</Label>
                <Slider
                  id="guidance"
                  min={1}
                  max={20}
                  step={0.5}
                  value={[guidanceScale]}
                  onValueChange={([value]) => setGuidanceScale(value)}
                />
                <p className="text-xs text-muted-foreground">How closely to follow the prompt</p>
              </div>

              {/* Generate Button */}
              <Button
                onClick={handleGenerate}
                disabled={loading}
                className="w-full gap-2"
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-5 w-5" />
                    Generate Image
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Preview */}
          <Card>
            <CardHeader>
              <CardTitle>Generated Image</CardTitle>
              <CardDescription>Your AI-generated artwork will appear here</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="aspect-square rounded-lg border-2 border-dashed border-border bg-muted/50 flex items-center justify-center overflow-hidden">
                {loading ? (
                  <div className="text-center space-y-4">
                    <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto" />
                    <p className="text-sm text-muted-foreground">Creating your image...</p>
                  </div>
                ) : generatedImage ? (
                  <img
                    src={generatedImage}
                    alt="Generated"
                    className="w-full h-full object-contain"
                  />
                ) : (
                  <div className="text-center space-y-2 p-8">
                    <ImageIcon className="h-16 w-16 text-muted-foreground/50 mx-auto" />
                    <p className="text-sm text-muted-foreground">
                      Enter a prompt and click generate
                    </p>
                  </div>
                )}
              </div>

              {generatedImage && !loading && (
                <Button
                  onClick={handleDownload}
                  variant="outline"
                  className="w-full mt-4 gap-2"
                >
                  <Download className="h-4 w-4" />
                  Download Image
                </Button>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
