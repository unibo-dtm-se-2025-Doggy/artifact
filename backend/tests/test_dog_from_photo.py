import io

from fastapi.testclient import TestClient

import backend.main as main


def dummy_file():
    return ("test.jpg", io.BytesIO(b"fake image bytes"), "image/jpeg")


def test_non_dog_returns_error(monkeypatch):
    client = TestClient(main.app)

    monkeypatch.setattr(main, "dog_model", type("M", (), {"is_dog": lambda _, __=None: False}))
    monkeypatch.setattr(main, "llm", object())

    resp = client.post("/api/dog-from-photo", files={"file": dummy_file()})
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

    monkeypatch.setattr(main, "dog_model", dog_model())
    monkeypatch.setattr(main, "llm", llm())

    resp = client.post("/api/dog-from-photo", files={"file": dummy_file()})
    data = resp.json()
    assert resp.status_code == 200
    assert data["breed"] == "husky"
    assert data["advice"] == "Advice for husky"
    assert data["raw_predictions"][0]["label"] == "husky"


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

    monkeypatch.setattr(main, "dog_model", dog_model())
    monkeypatch.setattr(main, "llm", llm())

    resp = client.post("/api/dog-from-photo", files={"file": dummy_file()})
    assert resp.status_code == 200
    assert resp.json()["error"] == "boom"
