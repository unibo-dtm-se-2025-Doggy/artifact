import os
import uuid

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.Features.DogRecognition.dog_recognition import DogRecognitionModel
from backend.Features.LLM.llm_engine import DogLLMEngine

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


# ---------- Init LLM ----------
llm: DogLLMEngine | None = None
try:
    llm = DogLLMEngine()
    print("LLM loaded successfully")
except Exception as e:
    print("LLM INIT ERROR:", e)


# ---------- Init Dog Recognition ----------
dog_model: DogRecognitionModel | None = None
try:
    dog_model = DogRecognitionModel()
    print("DogRecognition loaded successfully")
except Exception as e:
    print("DOG MODEL INIT ERROR:", e)


# ---------- TEXT ENDPOINT ----------
@app.get("/api/dog-advice")
def dog_advice(breed: str):
    if llm is None:
        return {"error": "LLM not initialized"}
    try:
        return {"advice": llm.generate_advice(breed)}
    except Exception as e:
        return {"error": str(e)}


# ---------- PHOTO ENDPOINT ----------
@app.post("/api/dog-from-photo")
async def dog_from_photo(file: UploadFile = File(...)):
    if dog_model is None:
        return {"error": "Dog recognition model not initialized"}
    if llm is None:
        return {"error": "LLM not initialized"}

    # --- 1. Save temp image ---
    temp_path = f"temp_{uuid.uuid4()}.jpg"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        # --- 2. Zero-shot dog check ---
        is_dog = dog_model.is_dog(temp_path)
        if not is_dog:
            return {"error": "Sorry, this is not a dog. Please try again"}

        # --- 3. Predict breed ---
        preds = dog_model.predict(temp_path)
        top_label = preds[0]["label"]

        # --- 4. Generate LLM advice ---
        advice = llm.generate_advice(top_label)

        return {"breed": top_label, "raw_predictions": preds, "advice": advice}

    except Exception as e:
        return {"error": str(e)}

    finally:
        # --- 5. Remove temp file ---
        if os.path.exists(temp_path):
            os.remove(temp_path)
