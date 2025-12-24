import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Video } from 'lucide-react';
import DashboardLayout from '@/components/DashboardLayout';
import { toast } from 'sonner';

export default function TextToVideo() {
  return (
    <DashboardLayout>
      <div className="container py-8 max-w-5xl">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-lg bg-gradient-to-br from-orange-500 to-red-500">
              <Video className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold">Text-to-Video</h1>
          </div>
          <p className="text-muted-foreground">
            Generate dynamic videos from text prompts with advanced video models
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Coming Soon</CardTitle>
            <CardDescription>This feature is under development</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Text-to-video generation will be available soon. You'll be able to:
            </p>
            <ul className="list-disc list-inside space-y-2 text-muted-foreground mb-6">
              <li>Generate videos from text descriptions</li>
              <li>Control video duration and frame rate</li>
              <li>Use multiple video generation models</li>
              <li>Download generated videos in MP4 format</li>
            </ul>
            <Button onClick={() => toast.info('Feature coming soon!')}>
              Notify Me When Ready
            </Button>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
