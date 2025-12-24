import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ImagePlay } from 'lucide-react';
import DashboardLayout from '@/components/DashboardLayout';
import { toast } from 'sonner';

export default function ImageToVideo() {
  return (
    <DashboardLayout>
      <div className="container py-8 max-w-5xl">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-lg bg-gradient-to-br from-green-500 to-emerald-500">
              <ImagePlay className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold">Image-to-Video</h1>
          </div>
          <p className="text-muted-foreground">
            Animate static images into captivating videos with motion prompts
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Coming Soon</CardTitle>
            <CardDescription>This feature is under development</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Image-to-video generation will be available soon. You'll be able to:
            </p>
            <ul className="list-disc list-inside space-y-2 text-muted-foreground mb-6">
              <li>Upload static images to animate</li>
              <li>Add motion prompts for controlled animation</li>
              <li>Adjust video duration and frame rate</li>
              <li>Create cinematic camera movements</li>
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
