import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/Hero";
import { DogAnalyzer } from "@/components/ImageUpload/DogAnalyzer";
import { Footer } from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen">
      <Navbar />
      
      <Hero />
      
      <section id="upload" className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto max-w-5xl space-y-12">
          <div className="text-center space-y-4">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground">
              Identify Your Dog's Breed
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Simply upload a clear photo of your dog, and our AI will instantly identify the breed and provide comprehensive care information.
            </p>
          </div>
          
          <DogAnalyzer />
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Index;
