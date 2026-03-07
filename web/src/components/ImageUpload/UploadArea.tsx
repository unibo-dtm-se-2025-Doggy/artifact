import { RefObject } from "react";
import { Upload } from "lucide-react";
import { Button } from "@/components/ui/button";

interface UploadAreaProps {
  fileInputRef: RefObject<HTMLInputElement>;
  isAnalyzing: boolean;
  onFileSelect: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export const UploadArea = ({ 
  fileInputRef, 
  isAnalyzing, 
  onFileSelect 
}: UploadAreaProps) => {
  return (
    <div>
      <div className="border-2 border-dashed border-border rounded-3xl p-16 text-center hover:border-primary hover:bg-primary/5 transition-all duration-300 group">
        <Upload className="w-16 h-16 mx-auto mb-6 text-muted-foreground group-hover:text-primary group-hover:scale-110 transition-all duration-300" />
        <h3 className="text-2xl font-bold mb-3 text-foreground">Upload Your Dog's Photo</h3>
        <p className="text-muted-foreground mb-8 max-w-md mx-auto">
          Choose a clear, well-lit photo showing your dog's face and body for the best results
        </p>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={onFileSelect}
          className="hidden"
          disabled={isAnalyzing}
        />
        <Button
          onClick={() => fileInputRef.current?.click()}
          size="lg"
          disabled={isAnalyzing}
          className="bg-gradient-to-r from-primary to-primary-glow hover:scale-105 shadow-soft transition-all duration-300 text-lg px-8 py-6 h-auto"
        >
          <Upload className="w-5 h-5 mr-2" />
          Choose File
        </Button>
      </div>
    </div>
  );
};
