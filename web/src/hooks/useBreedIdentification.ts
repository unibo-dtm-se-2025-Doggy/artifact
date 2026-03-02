import { useState } from "react";

const API_URL = "http://127.0.0.1:8000/api/dog-from-photo";

export const useBreedIdentification = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const identifyBreed = async (file: File, preview: string) => {
    setIsAnalyzing(true);
    setResult(null);
    setError(null);

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

      if (data.error) {
        throw new Error(data.error);
      }

      setResult({
        breed: data.breed,
        advice: data.advice,
      });

    } catch (e: any) {
      const message = e?.message || "Failed to analyze image";
      setError(message);

    } finally {
      setIsAnalyzing(false);
    }
  };

  return {
    isAnalyzing,
    result,
    error,
    identifyBreed,
  };
};
