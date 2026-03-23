from importlib import import_module

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    # Running as package: python -m uvicorn backend.main:app
    router_module = import_module("backend.Core.router")
except ModuleNotFoundError:
    # Running from backend dir: uvicorn main:app
    router_module = import_module("Core.router")

app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Health Check ----------
@app.get("/")
def root():
    return {"status": "ok", "message": "backend is running"}


app.include_router(router_module.router)
