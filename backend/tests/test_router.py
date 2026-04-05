from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_router_dog_advice(monkeypatch):
    class FakeLLM:
        def generate_advice(self, breed: str):
            return f"Advice for {breed}"

    import backend.Core.router as router

    monkeypatch.setattr(router, "llm", FakeLLM())
    monkeypatch.setattr(router, "llm_init_error", None)

    app = FastAPI()
    app.include_router(router.router)

    client = TestClient(app)
    resp = client.get("/dog-advice", params={"breed": "husky"})

    assert resp.status_code == 200
    assert resp.json()["advice"] == "Advice for husky"
