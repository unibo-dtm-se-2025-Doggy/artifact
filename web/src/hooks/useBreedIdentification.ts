import { useState } from "react";
import { type BreedIdentificationResult, type IDogApiClient, dogApiClient } from "@/integrations/dogApi";

export type { BreedIdentificationResult };

export const useBreedIdentification = (client: IDogApiClient = dogApiClient) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<BreedIdentificationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const identifyBreed = async (file: File, _preview: string) => {
    setIsAnalyzing(true);
    setResult(null);
    setError(null);

    try {
      const data = await client.identifyBreed(file);
      setResult(data);
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : "Failed to analyze image";
      setError(message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return { isAnalyzing, result, error, identifyBreed };
};
