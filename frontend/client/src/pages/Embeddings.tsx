import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Binary } from 'lucide-react';
import DashboardLayout from '@/components/DashboardLayout';
import { toast } from 'sonner';

export default function Embeddings() {
  return (
    <DashboardLayout>
      <div className="container py-8 max-w-5xl">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-lg bg-gradient-to-br from-yellow-500 to-orange-500">
              <Binary className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold">Embeddings</h1>
          </div>
          <p className="text-muted-foreground">
            Generate vector embeddings for semantic search and similarity analysis
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Coming Soon</CardTitle>
            <CardDescription>This feature is under development</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Text embedding generation will be available soon. You'll be able to:
            </p>
            <ul className="list-disc list-inside space-y-2 text-muted-foreground mb-6">
              <li>Generate vector embeddings from text</li>
              <li>Choose from multiple embedding models</li>
              <li>Use embeddings for semantic search</li>
              <li>Calculate text similarity scores</li>
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
