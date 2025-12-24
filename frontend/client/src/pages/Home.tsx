import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Link } from 'wouter';
import {
  Image,
  Wand2,
  Mic,
  AudioLines,
  MessageSquare,
  Binary,
  Video,
  ImagePlay,
  ArrowRight,
  Sparkles,
  Zap,
  Shield
} from 'lucide-react';

const features = [
  {
    name: 'Image Generation',
    description: 'Create stunning images from text descriptions using Stable Diffusion models',
    icon: Image,
    href: '/image-generation',
    color: 'from-purple-500 to-pink-500',
  },
  {
    name: 'Image Editing',
    description: 'Edit and enhance images with AI-powered inpainting and transformations',
    icon: Wand2,
    href: '/image-editing',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    name: 'Text-to-Video',
    description: 'Generate dynamic videos from text prompts with advanced video models',
    icon: Video,
    href: '/text-to-video',
    color: 'from-orange-500 to-red-500',
  },
  {
    name: 'Image-to-Video',
    description: 'Animate static images into captivating videos with motion prompts',
    icon: ImagePlay,
    href: '/image-to-video',
    color: 'from-green-500 to-emerald-500',
  },
  {
    name: 'Text-to-Speech',
    description: 'Convert text to natural-sounding speech in multiple languages',
    icon: AudioLines,
    href: '/text-to-speech',
    color: 'from-indigo-500 to-purple-500',
  },
  {
    name: 'Speech-to-Text',
    description: 'Transcribe audio files with high accuracy using Whisper',
    icon: Mic,
    href: '/speech-to-text',
    color: 'from-pink-500 to-rose-500',
  },
  {
    name: 'AI Chat',
    description: 'Interact with state-of-the-art language models for intelligent conversations',
    icon: MessageSquare,
    href: '/chat',
    color: 'from-cyan-500 to-blue-500',
  },
  {
    name: 'Embeddings',
    description: 'Generate vector embeddings for semantic search and similarity analysis',
    icon: Binary,
    href: '/embeddings',
    color: 'from-yellow-500 to-orange-500',
  },
];

const highlights = [
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Optimized for speed with automatic retry and caching',
  },
  {
    icon: Shield,
    title: 'Production Ready',
    description: 'Robust error handling and comprehensive logging',
  },
  {
    icon: Sparkles,
    title: 'Multiple Models',
    description: 'Access to various HuggingFace AI models',
  },
];

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-accent/10 to-background" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(120,119,198,0.15),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(74,222,128,0.1),transparent_50%)]" />
        
        <div className="relative container py-24 lg:py-32">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            {/* Badge */}
            <Badge variant="secondary" className="px-4 py-2 text-sm font-medium">
              <Sparkles className="h-4 w-4 mr-2 inline" />
              Powered by HuggingFace AI Models
            </Badge>

            {/* Heading */}
            <h1 className="text-5xl lg:text-7xl font-bold tracking-tight">
              <span className="bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent animate-gradient">
                AI Platform
              </span>
              <br />
              <span className="text-foreground">Dashboard</span>
            </h1>

            {/* Description */}
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              A unified interface for multiple AI capabilities. Generate images, create videos, 
              synthesize speech, transcribe audio, and interact with language models—all in one place.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <Link href="/image-generation">
                <Button size="lg" className="gap-2 shadow-lg shadow-primary/25">
                  Get Started
                  <ArrowRight className="h-5 w-5" />
                </Button>
              </Link>
              <Button size="lg" variant="outline" className="gap-2">
                View Documentation
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Highlights Section */}
      <section className="py-16 border-y border-border bg-card/50">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {highlights.map((item) => {
              const Icon = item.icon;
              return (
                <div key={item.title} className="flex items-start gap-4">
                  <div className="p-3 rounded-lg bg-primary/10">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg mb-1">{item.title}</h3>
                    <p className="text-sm text-muted-foreground">{item.description}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-24">
        <div className="container">
          <div className="text-center mb-16 space-y-4">
            <h2 className="text-4xl font-bold">Explore AI Capabilities</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Choose from our suite of AI-powered tools to bring your ideas to life
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <Link key={feature.name} href={feature.href}>
                  <Card className="group cursor-pointer transition-all duration-300 hover:shadow-xl hover:shadow-primary/10 hover:-translate-y-1 border-border/50 hover:border-primary/50 h-full">
                    <CardHeader>
                      <div className="mb-4">
                        <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${feature.color} shadow-lg`}>
                          <Icon className="h-6 w-6 text-white" />
                        </div>
                      </div>
                      <CardTitle className="text-xl group-hover:text-primary transition-colors">
                        {feature.name}
                      </CardTitle>
                      <CardDescription className="text-sm leading-relaxed">
                        {feature.description}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center text-sm font-medium text-primary group-hover:gap-2 transition-all">
                        Try it now
                        <ArrowRight className="h-4 w-4 ml-1 group-hover:translate-x-1 transition-transform" />
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-12 bg-card/30">
        <div className="container">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="bg-gradient-to-br from-primary to-accent p-2 rounded-lg">
                <Sparkles className="h-5 w-5 text-primary-foreground" />
              </div>
              <span className="font-semibold">AI Platform</span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2025 AI Platform. Powered by HuggingFace.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
