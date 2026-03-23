import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)


class DogLLMEngine:
    def __init__(self):
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise ValueError("HF_TOKEN is not set in backend/.env")

        # Check https://huggingface.co/inference/models for supported alternatives
        self.model_name = "openai/gpt-oss-20b"

        self.client = InferenceClient(token=hf_token)

    def generate_advice(self, breed: str) -> str:
        prompt = f"""
You are DogExpertGPT, a veterinarian and dog behavior specialist.
Write exactly 6 short lines about this breed: {breed}.
Do not use markdown, bold text, headings, or extra intro text.
Each line must start with an emoji and the category name.
Keep each line concise and practical.

Use exactly this format:
🐶 Temperament: ...
❤️ Common health risks: ...
🍖 Feeding recommendations: ...
🏃 Activity needs: ...
🛁 Grooming needs: ...
🎓 Training tips: ...
"""

        response = self.client.chat_completion(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise dog expert. Follow the output format exactly.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.3,
        )

        content = response.choices[0].message.get("content", "")
        return str(content) if content is not None else ""
