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

    import backend.Features.DogRecognition.dog_recognition as dog_recognition_module
    import backend.Features.LLM.llm_engine as llm_engine_module

    monkeypatch.setattr(dog_recognition_module, "DogRecognitionModel", FakeDogModel)
    monkeypatch.setattr(llm_engine_module, "DogLLMEngine", FakeLLM)

    # Force a fresh import so the router binds the patched classes.
    sys.modules.pop("backend.Core.router", None)
    import backend.Core.router as router

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
