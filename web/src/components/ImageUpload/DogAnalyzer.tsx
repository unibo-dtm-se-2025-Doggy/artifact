import { useState } from "react";
import { Loader2 } from "lucide-react";

import { ImageUpload } from "@/components/ImageUpload";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Card } from "@/components/ui/card";

const API_URL = "http://127.0.0.1:8000/api/dog-from-photo";

interface BreedResult {
  breed: string;
  advice: string;
}

export const DogAnalyzer = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<BreedResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelected = async (file: File, _preview: string) => {
    setError(null);
    setResult(null);
    setIsAnalyzing(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.error || `AI server error: ${response.status}`);
      }

      const data = await response.json();

      setResult({
        breed: data.breed,
        advice: data.advice,
      });
    } catch (e: any) {
      setError(e?.message || "Failed to analyze the image");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="space-y-8">
      <ImageUpload onImageSelected={handleImageSelected} isAnalyzing={isAnalyzing} />

      <Card className="space-y-4 p-6">
        <h2 className="text-2xl font-bold">Dog Analysis</h2>

        {isAnalyzing && (
          <div className="flex items-center gap-3 text-muted-foreground">
            <Loader2 className="h-5 w-5 animate-spin" />
            <span>Analyzing your dog photo...</span>
          </div>
        )}

        {error && (
          <Alert variant="destructive">
            <AlertTitle>AI Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {result?.breed && (
          <div>
            <h3 className="text-lg font-semibold">
              Detected breed:
              <span className="ml-2 text-primary">{result.breed}</span>
            </h3>
          </div>
        )}

        {result?.advice && (
          <div>
            <h4 className="mb-2 font-semibold">AI recommendations:</h4>
            <p className="whitespace-pre-line text-muted-foreground">{result.advice}</p>
          </div>
        )}
      </Card>
    </div>
  );
};
