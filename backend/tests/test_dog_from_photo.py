import io

from fastapi.testclient import TestClient

import backend.Core.router as api_router
import backend.main as main


def dummy_file():
    return ("test.jpg", io.BytesIO(b"fake image bytes"), "image/jpeg")


def test_non_dog_returns_error(monkeypatch):
    client = TestClient(main.app)

    monkeypatch.setattr(
        api_router, "dog_model", type("M", (), {"is_dog": lambda _, __=None: False})()
    )
    monkeypatch.setattr(api_router, "dog_model_init_error", None)
    monkeypatch.setattr(api_router, "llm", object())
    monkeypatch.setattr(api_router, "llm_init_error", None)

    resp = client.post("/api/v1/dog-from-photo", files={"file": dummy_file()})
    assert resp.status_code == 200
    assert resp.json()["error"] == "Sorry, this is not a dog. Please try again"


def test_dog_returns_breed_and_advice(monkeypatch):
    client = TestClient(main.app)

    dog_model = type(
        "DogModel",
        (),
        {
            "is_dog": lambda _, __: True,
            "predict": lambda _, __: [{"label": "husky", "score": 0.9}],
        },
    )
    llm = type("LLM", (), {"generate_advice": lambda _, breed: f"Advice for {breed}"})

    monkeypatch.setattr(api_router, "dog_model", dog_model())
    monkeypatch.setattr(api_router, "dog_model_init_error", None)
    monkeypatch.setattr(api_router, "llm", llm())
    monkeypatch.setattr(api_router, "llm_init_error", None)

    resp = client.post("/api/v1/dog-from-photo", files={"file": dummy_file()})
    data = resp.json()
    assert resp.status_code == 200
    assert data["breed"] == "husky"
    assert data["advice"] == "Advice for husky"
    assert data["raw_predictions"][0]["label"] == "husky"


def test_dog_aliases_are_normalized(monkeypatch):
    client = TestClient(main.app)

    dog_model = type(
        "DogModel",
        (),
        {
            "is_dog": lambda _, __: True,
            "predict": lambda _, __: [
                {
                    "label": "German shepherd, German shepherd dog, German police dog, alsatian",
                    "score": 0.9,
                }
            ],
        },
    )
    llm = type("LLM", (), {"generate_advice": lambda _, breed: f"Advice for {breed}"})

    monkeypatch.setattr(api_router, "dog_model", dog_model())
    monkeypatch.setattr(api_router, "dog_model_init_error", None)
    monkeypatch.setattr(api_router, "llm", llm())
    monkeypatch.setattr(api_router, "llm_init_error", None)

    resp = client.post("/api/v1/dog-from-photo", files={"file": dummy_file()})
    data = resp.json()
    assert resp.status_code == 200
    assert data["breed"] == "German shepherd"
    assert data["advice"] == "Advice for German shepherd"


def test_predict_exception_is_returned(monkeypatch):
    client = TestClient(main.app)

    dog_model = type(
        "DogModel",
        (),
        {
            "is_dog": lambda _, __: True,
            "predict": lambda _, __: (_ for _ in ()).throw(RuntimeError("boom")),
        },
    )
    llm = type("LLM", (), {"generate_advice": lambda _, __: "advice"})

    monkeypatch.setattr(api_router, "dog_model", dog_model())
    monkeypatch.setattr(api_router, "dog_model_init_error", None)
    monkeypatch.setattr(api_router, "llm", llm())
    monkeypatch.setattr(api_router, "llm_init_error", None)

    resp = client.post("/api/v1/dog-from-photo", files={"file": dummy_file()})
    assert resp.status_code == 200
    assert resp.json()["error"] == "boom"
