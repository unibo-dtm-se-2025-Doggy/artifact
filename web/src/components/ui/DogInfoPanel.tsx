import { Card } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";

interface Props {
  result: {
    breed: string;
    advice: string;
  } | null;
  isAnalyzing: boolean;
  error: string | null;
}

export const DogInfoPanel = ({ result, isAnalyzing, error }: Props) => {
  return (
    <Card className="p-6 min-h-[260px] space-y-4">
      <h2 className="text-xl font-semibold">Dog Analysis</h2>

      {/* 1. Analysing */}
      {isAnalyzing && (
        <div className="flex items-center gap-2 text-muted-foreground">
          <Loader2 className="w-4 h-4 animate-spin" />
          Analyzing your dog photo...
        </div>
      )}

      {!isAnalyzing && error && (
        <Alert variant="destructive">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {!isAnalyzing && !error && !result && (
        <p className="text-muted-foreground">
          Upload a clear photo of your dog above.
          <br />
          The detected breed and AI-generated tips will appear here.
        </p>
      )}
      
      {!isAnalyzing && !error && result && (
        <div className="space-y-4">
          <div>
            <p className="text-xs uppercase text-muted-foreground">
              Detected breed
            </p>
            <p className="text-2xl font-bold text-primary">{result.breed}</p>
          </div>

          <div>
            <h3 className="font-semibold mb-1">AI recommendations</h3>
            <p className="whitespace-pre-line leading-relaxed">
              {result.advice}
            </p>
          </div>
        </div>
      )}
    </Card>
  );
};
