from typing import Any

from PIL import Image
from transformers import pipeline


class DogRecognitionModel:
    def __init__(self) -> None:
        # Zero-shot check to ensure the photo contains a dog
        self.zero_shot_model = pipeline(
            "zero-shot-image-classification",
            model="openai/clip-vit-base-patch32",
        )
        self.zero_shot_labels = ["dog", "not dog"]

        # Breed classifier
        self.model = pipeline(
            "image-classification",
            model="google/vit-base-patch16-224",
        )

    def is_dog(self, image_path: str) -> bool:
        """Return True if the CLIP zero-shot classifier thinks the image is a dog."""
        img = Image.open(image_path)
        results: list[dict[str, Any]] = self.zero_shot_model(
            images=img,
            candidate_labels=self.zero_shot_labels,
        )
        top_label = results[0]["label"]
        return str(top_label) == "dog"

    def predict(self, image_path: str):
        """Return the top 3 breed predictions for the given image."""
        img = Image.open(image_path)
        results = self.model(img)
        return results[:3]
