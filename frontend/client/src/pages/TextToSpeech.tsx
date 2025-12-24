import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AudioLines } from 'lucide-react';
import DashboardLayout from '@/components/DashboardLayout';
import { toast } from 'sonner';

export default function TextToSpeech() {
  return (
    <DashboardLayout>
      <div className="container py-8 max-w-5xl">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-500">
              <AudioLines className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold">Text-to-Speech</h1>
          </div>
          <p className="text-muted-foreground">
            Convert text to natural-sounding speech in multiple languages
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Coming Soon</CardTitle>
            <CardDescription>This feature is under development</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Text-to-speech synthesis will be available soon. You'll be able to:
            </p>
            <ul className="list-disc list-inside space-y-2 text-muted-foreground mb-6">
              <li>Convert text to natural-sounding speech</li>
              <li>Choose from multiple voice models</li>
              <li>Adjust speech speed and tone</li>
              <li>Download audio in WAV format</li>
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
