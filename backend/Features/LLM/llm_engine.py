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

        # 100% рабочая модель
        self.model_name = "deepseek-ai/DeepSeek-V3.2:fireworks-ai"

        self.client = InferenceClient(token=hf_token)

    def generate_advice(self, breed: str) -> str:
        prompt = f"""
You are DogExpertGPT, a veterinarian and dog behavior specialist.
Provide a short bullet list about this breed: {breed}.

List:
- Temperament
- Common health risks
- Feeding recommendations
- Activity needs
- Grooming needs
- Training tips
"""

        response = self.client.chat_completion(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a concise dog expert."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.3,
        )

        content = response.choices[0].message.get("content", "")
        return str(content) if content is not None else ""
