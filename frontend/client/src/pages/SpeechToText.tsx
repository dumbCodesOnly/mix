import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Mic } from 'lucide-react';
import DashboardLayout from '@/components/DashboardLayout';
import { toast } from 'sonner';

export default function SpeechToText() {
  return (
    <DashboardLayout>
      <div className="container py-8 max-w-5xl">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-lg bg-gradient-to-br from-pink-500 to-rose-500">
              <Mic className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold">Speech-to-Text</h1>
          </div>
          <p className="text-muted-foreground">
            Transcribe audio files with high accuracy using Whisper
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Coming Soon</CardTitle>
            <CardDescription>This feature is under development</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Speech-to-text transcription will be available soon. You'll be able to:
            </p>
            <ul className="list-disc list-inside space-y-2 text-muted-foreground mb-6">
              <li>Upload audio files for transcription</li>
              <li>Record audio directly in the browser</li>
              <li>Choose from multiple Whisper models</li>
              <li>Get accurate transcriptions with confidence scores</li>
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
