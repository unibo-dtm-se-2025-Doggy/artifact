import os
import uuid

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

try:
    # Running as package: python -m uvicorn backend.main:app
    from backend.Features.DogRecognition.dog_recognition import DogRecognitionModel
    from backend.Features.LLM.llm_engine import DogLLMEngine
except ModuleNotFoundError:
    # Running from backend dir: uvicorn main:app
    from Features.DogRecognition.dog_recognition import DogRecognitionModel
    from Features.LLM.llm_engine import DogLLMEngine

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


def _normalize_breed_label(label: str) -> str:
    """Keep only the primary breed name when the classifier returns aliases."""
    return label.split(",")[0].strip()


llm: DogLLMEngine | None = None
llm_init_error: str | None = None

dog_model: DogRecognitionModel | None = None
dog_model_init_error: str | None = None


def _get_llm() -> DogLLMEngine | None:
    global llm, llm_init_error

    if llm is not None or llm_init_error is not None:
        return llm

    try:
        llm = DogLLMEngine()
        print("LLM loaded successfully")
    except Exception as e:
        llm_init_error = str(e)
        print("LLM INIT ERROR:", e)

    return llm


def _get_dog_model() -> DogRecognitionModel | None:
    global dog_model, dog_model_init_error

    if dog_model is not None or dog_model_init_error is not None:
        return dog_model

    try:
        dog_model = DogRecognitionModel()
        print("DogRecognition loaded successfully")
    except Exception as e:
        dog_model_init_error = str(e)
        print("DOG MODEL INIT ERROR:", e)

    return dog_model


# ---------- TEXT ENDPOINT ----------
@app.get("/api/dog-advice")
def dog_advice(breed: str):
    llm_instance = _get_llm()
    if llm_instance is None:
        return {"error": llm_init_error or "LLM not initialized"}

    try:
        return {"advice": llm_instance.generate_advice(breed)}
    except Exception as e:
        return {"error": str(e)}


# ---------- PHOTO ENDPOINT ----------
@app.post("/api/dog-from-photo")
async def dog_from_photo(file: UploadFile = File(...)):
    model_instance = _get_dog_model()
    if model_instance is None:
        return {"error": dog_model_init_error or "Dog recognition model not initialized"}

    llm_instance = _get_llm()
    if llm_instance is None:
        return {"error": llm_init_error or "LLM not initialized"}

    # --- 1. Save temp image ---
    temp_path = f"temp_{uuid.uuid4()}.jpg"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        # --- 2. Zero-shot dog check ---
        is_dog = model_instance.is_dog(temp_path)
        if not is_dog:
            return {"error": "Sorry, this is not a dog. Please try again"}

        # --- 3. Predict breed ---
        preds = model_instance.predict(temp_path)
        top_label = _normalize_breed_label(preds[0]["label"])

        # --- 4. Generate LLM advice ---
        advice = llm_instance.generate_advice(top_label)

        return {"breed": top_label, "raw_predictions": preds, "advice": advice}

    except Exception as e:
        return {"error": str(e)}

    finally:
        # --- 5. Remove temp file ---
        if os.path.exists(temp_path):
            os.remove(temp_path)
