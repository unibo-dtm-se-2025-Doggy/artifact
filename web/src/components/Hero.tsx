import { Button } from "@/components/ui/button";
import { Sparkles, Heart } from "lucide-react";
import { Link } from "react-router-dom";

export const Hero = () => {
  const scrollToUpload = () => {
    const uploadSection = document.getElementById('upload');
    uploadSection?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className="relative min-h-[90vh] flex items-center overflow-hidden bg-gradient-to-br from-secondary via-background to-background">
      <div className="container mx-auto px-4 py-20 md:py-32">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Left side - Content */}
          <div className="space-y-8 animate-fade-in">
            <div className="inline-block">
              <span className="text-sm font-semibold text-primary uppercase tracking-wider bg-primary/10 px-4 py-2 rounded-full">
                AI-Powered Breed Identification
              </span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold leading-tight">
              <span className="text-foreground">Discover Your</span>
              <br />
              <span className="bg-gradient-to-r from-primary to-primary-glow bg-clip-text text-transparent">
                Dog's Breed
              </span>
            </h1>
            
            <p className="text-lg md:text-xl text-muted-foreground leading-relaxed max-w-lg">
              Upload a photo and get instant breed identification with personalized care recommendations, nutrition advice, and grooming tips.
            </p>

            <div className="flex flex-wrap gap-4">
              <Button 
                size="lg" 
                onClick={scrollToUpload}
                className="bg-gradient-to-r from-primary to-primary-glow hover:opacity-90 shadow-soft text-lg px-8 py-6 h-auto"
              >
                Try It Now
              </Button>
              <Link to="/how-it-works">
                <Button 
                  size="lg" 
                  variant="outline"
                  className="border-2 text-lg px-8 py-6 h-auto hover:bg-primary/5"
                >
                  Learn More
                </Button>
              </Link>
            </div>

            <div className="flex flex-wrap gap-6 pt-4">
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <p className="font-semibold text-foreground">Instant Results</p>
                  <p className="text-sm text-muted-foreground">AI-powered analysis</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                  <Heart className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <p className="font-semibold text-foreground">Care Tips</p>
                  <p className="text-sm text-muted-foreground">Personalized advice</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right side - Image placeholder */}
          <div className="relative animate-slide-up">
            <div className="relative rounded-3xl overflow-hidden shadow-float">
              <div className="aspect-square bg-gradient-to-br from-primary/20 to-primary-glow/20 backdrop-blur-sm flex items-center justify-center">
                <img 
                  src="https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800&q=80" 
                  alt="Happy dog" 
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="absolute -bottom-4 -right-4 w-32 h-32 bg-primary rounded-3xl rotate-12 opacity-20 blur-2xl" />
              <div className="absolute -top-4 -left-4 w-40 h-40 bg-primary-glow rounded-3xl -rotate-12 opacity-20 blur-2xl" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
