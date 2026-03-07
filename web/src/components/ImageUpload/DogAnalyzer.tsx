import { useState } from "react";
import { ImageUpload } from "@/components/ImageUpload";
import { Card } from "@/components/ui/card";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Loader2 } from "lucide-react";

const API_URL = "http://127.0.0.1:8000/api/dog-from-photo";
const getErrorMessage = (data: any): string | null => {
  if (data?.error) {
    return data.error;
  }
  const detail = data?.detail;
  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0];
    if (first?.msg) {
      return String(first.msg);
    }
  }
  return null;
};

interface BreedResult {
  breed: string;
  advice: string;
  raw_predictions?: { label: string; score: number }[];
}

export const DogAnalyzer = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<BreedResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelected = async (file: File, preview: string) => {
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
      const apiError = getErrorMessage(data);
      if (apiError) {
        throw new Error(apiError);
      }

      setResult({
        breed: data.breed,
        advice: data.advice,
        raw_predictions: data.raw_predictions,
      });
    } catch (e: any) {
      setError(e?.message || "Failed to analyze the image");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* ЗАГРУЗКА КАРТИНКИ */}
      <ImageUpload
        onImageSelected={handleImageSelected}
        isAnalyzing={isAnalyzing}
      />

      {/* ПОСТОЯННОЕ ОКНО ВЫВОДА */}
      <Card className="p-6 space-y-4">
        <h2 className="text-2xl font-bold">
          Dog Analysis
        </h2>

        {isAnalyzing && (
          <div className="flex items-center gap-3 text-muted-foreground">
            <Loader2 className="w-5 h-5 animate-spin" />
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
            <h3 className="font-semibold text-lg">
              Detected breed:
              <span className="text-primary ml-2">{result.breed}</span>
            </h3>
          </div>
        )}

        {result?.raw_predictions && (
          <div className="text-sm text-muted-foreground">
            <h4 className="font-semibold mb-1">Top predictions:</h4>
            <ul className="list-disc list-inside">
              {result.raw_predictions.map((p, idx) => (
                <li key={idx}>
                  {p.label} — {(p.score * 100).toFixed(1)}%
                </li>
              ))}
            </ul>
          </div>
        )}

        {result?.advice && (
          <div>
            <h4 className="font-semibold mb-2">AI recommendations:</h4>
            <p className="whitespace-pre-line text-muted-foreground">
              {result.advice}
            </p>
          </div>
        )}
      </Card>
    </div>
  );
};
