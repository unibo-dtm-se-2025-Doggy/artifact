import { useState } from "react";


const API_URL = `${import.meta.env.VITE_API_BASE_URL}/api/dog-from-photo`;
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
