import { ImageUpload } from "@/components/ImageUpload";
import { useBreedIdentification } from "@/hooks/useBreedIdentification";
import { DogInfoPanel } from "@/components/ui/DogInfoPanel";

export const DogAnalyzer = () => {
  const { isAnalyzing, identifyBreed, result, error } = useBreedIdentification();

  return (
    <>
      <ImageUpload onImageSelected={identifyBreed} isAnalyzing={isAnalyzing} />
      <DogInfoPanel result={result} isAnalyzing={isAnalyzing} error={error} />
    </>
  );
};
