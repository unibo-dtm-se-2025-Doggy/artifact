import { useState, useRef } from "react";
import { Card } from "@/components/ui/card";
import { UploadArea } from "./ImageUpload/UploadArea";
import { PreviewArea } from "./ImageUpload/PreviewArea";

interface ImageUploadProps {
  onImageSelected: (file: File, preview: string) => void;
  isAnalyzing: boolean;
}

export const ImageUpload = ({ onImageSelected, isAnalyzing }: ImageUploadProps) => {
  const [preview, setPreview] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const result = reader.result as string;
        setPreview(result);
        onImageSelected(file, result);
      };
      reader.readAsDataURL(file);
    }
  };

  const clearImage = () => {
    setPreview("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <Card className="p-8 md:p-12 shadow-soft animate-slide-up bg-card border-2 hover:shadow-float transition-all duration-300">
      {!preview ? (
        <UploadArea
          fileInputRef={fileInputRef}
          isAnalyzing={isAnalyzing}
          onFileSelect={handleFileSelect}
        />
      ) : (
        <PreviewArea
          preview={preview}
          isAnalyzing={isAnalyzing}
          onClear={clearImage}
        />
      )}
    </Card>
  );
};
