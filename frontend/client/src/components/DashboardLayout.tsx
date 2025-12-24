import { Link, useLocation } from 'wouter';
import { 
  Image, 
  Wand2, 
  Mic, 
  AudioLines, 
  MessageSquare, 
  Binary,
  Video,
  ImagePlay,
  Sparkles,
  Menu,
  X
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { useState } from 'react';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const navigation = [
  { name: 'Image Generation', href: '/image-generation', icon: Image },
  { name: 'Image Editing', href: '/image-editing', icon: Wand2 },
  { name: 'Text-to-Video', href: '/text-to-video', icon: Video },
  { name: 'Image-to-Video', href: '/image-to-video', icon: ImagePlay },
  { name: 'Text-to-Speech', href: '/text-to-speech', icon: AudioLines },
  { name: 'Speech-to-Text', href: '/speech-to-text', icon: Mic },
  { name: 'AI Chat', href: '/chat', icon: MessageSquare },
  { name: 'Embeddings', href: '/embeddings', icon: Binary },
];

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [location] = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile menu button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <Button
          variant="outline"
          size="icon"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="bg-card/80 backdrop-blur-sm"
        >
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </Button>
      </div>

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-40 w-72 bg-card border-r border-border transform transition-transform duration-200 ease-in-out lg:translate-x-0',
          mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="px-6 py-8 border-b border-border">
            <Link href="/" onClick={() => setMobileMenuOpen(false)}>
              <div className="flex items-center gap-3 group cursor-pointer">
                <div className="relative">
                  <div className="absolute inset-0 bg-primary/20 blur-xl rounded-full" />
                  <div className="relative bg-gradient-to-br from-primary to-accent p-2.5 rounded-xl">
                    <Sparkles className="h-6 w-6 text-primary-foreground" />
                  </div>
                </div>
                <div>
                  <h1 className="text-xl font-bold text-foreground group-hover:text-primary transition-colors">
                    AI Platform
                  </h1>
                  <p className="text-xs text-muted-foreground">Powered by HuggingFace</p>
                </div>
              </div>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
            {navigation.map((item) => {
              const isActive = location === item.href;
              const Icon = item.icon;
              
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <div
                    className={cn(
                      'flex items-center gap-3 px-4 py-3 rounded-lg transition-all cursor-pointer group',
                      isActive
                        ? 'bg-primary text-primary-foreground shadow-lg shadow-primary/25'
                        : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                    )}
                  >
                    <Icon className={cn(
                      'h-5 w-5 transition-transform group-hover:scale-110',
                      isActive && 'animate-pulse'
                    )} />
                    <span className="font-medium">{item.name}</span>
                  </div>
                </Link>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-border">
            <div className="text-xs text-muted-foreground space-y-1">
              <p>Version 1.0.0</p>
              <p>© 2025 AI Platform</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Mobile overlay */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 bg-background/80 backdrop-blur-sm z-30 lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Main content */}
      <main className="lg:pl-72">
        <div className="min-h-screen">
          {children}
        </div>
      </main>
    </div>
  );
}
