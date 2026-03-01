import importlib
import os
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_router_predict(monkeypatch):
    monkeypatch.setenv("HF_TOKEN", "dummy-token")

    class FakeDogModel:
        def is_dog(self, *_):
            return True

        def predict(self, *_):
            return [{"label": "husky", "score": 0.9}]

    class FakeLLM:
        def generate_advice(self, breed: str):
            return f"Advice for {breed}"

    # Убираем кеши, где могли быть реальные импорты
    for mod in list(sys.modules):
        if mod.startswith("backend.Features."):
            sys.modules.pop(mod)

    # Патчим оба пути импортов
    monkeypatch.setattr(
        "backend.Features.DogRecognition.dog_recognition.DogRecognitionModel",
        FakeDogModel,
        raising=False,
    )
    monkeypatch.setattr(
        "backend.Features.LLM.llm_engine.DogLLMEngine",
        FakeLLM,
        raising=False,
    )

    import backend.Core.router as router

    importlib.reload(router)

    router.ml_model = FakeDogModel()
    router.llm_engine = FakeLLM()

    app = FastAPI()
    app.include_router(router.router)

    client = TestClient(app)
    resp = client.post("/predict", files={"file": ("test.jpg", b"fake", "image/jpeg")})

    assert resp.status_code == 200
    assert resp.json()["predictions"][0]["label"] == "husky"

    uploaded_path = "uploaded_test.jpg"
    if os.path.exists(uploaded_path):
        os.remove(uploaded_path)
