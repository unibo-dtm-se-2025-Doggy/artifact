import pytest

import backend.Features.LLM.llm_engine as llm_engine
from backend.Features.LLM.llm_engine import DogLLMEngine


def test_llm_engine_requires_token(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    with pytest.raises(ValueError):
        DogLLMEngine()


def test_llm_engine_generate_advice(monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "dummy-token")

    class FakeInferenceClient:
        def __init__(self, token=None):
            self.token = token

        def chat_completion(self, model=None, messages=None, max_tokens=None, temperature=None):
            class Choice:
                def __init__(self):
                    self.message = {"content": "Here are bullet points"}

            class Response:
                def __init__(self):
                    self.choices = [Choice()]

            return Response()

    monkeypatch.setattr(llm_engine, "InferenceClient", FakeInferenceClient)

    engine = DogLLMEngine()
    advice = engine.generate_advice("husky")
    assert "bullet" in advice.lower()
