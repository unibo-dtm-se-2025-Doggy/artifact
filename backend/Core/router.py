from __future__ import annotations

import os
import uuid
from importlib import import_module
from typing import Any

from fastapi import APIRouter, File, UploadFile

try:
    from backend.Core.interfaces import IDogLLMEngine, IDogRecognitionModel
except ModuleNotFoundError:
    from Core.interfaces import IDogLLMEngine, IDogRecognitionModel  # type: ignore[no-redef]

try:
    # Running as package: python -m uvicorn backend.main:app
    dog_recognition_module: Any = import_module("backend.Features.DogRecognition.dog_recognition")
    llm_engine_module: Any = import_module("backend.Features.LLM.llm_engine")
except ModuleNotFoundError:
    # Running from backend dir: uvicorn main:app
    dog_recognition_module = import_module("Features.DogRecognition.dog_recognition")
    llm_engine_module = import_module("Features.LLM.llm_engine")

router = APIRouter()

llm: IDogLLMEngine | None = None
llm_init_error: str | None = None

dog_model: IDogRecognitionModel | None = None
dog_model_init_error: str | None = None


def _normalize_breed_label(label: str) -> str:
    """Keep only the primary breed name when the classifier returns aliases."""
    return label.split(",")[0].strip()


def _get_llm() -> IDogLLMEngine | None:
    global llm, llm_init_error

    if llm is not None or llm_init_error is not None:
        return llm

    try:
        llm = llm_engine_module.DogLLMEngine()
        print("LLM loaded successfully")
    except Exception as e:
        llm_init_error = str(e)
        print("LLM INIT ERROR:", e)

    return llm


def _get_dog_model() -> IDogRecognitionModel | None:
    global dog_model, dog_model_init_error

    if dog_model is not None or dog_model_init_error is not None:
        return dog_model

    try:
        dog_model = dog_recognition_module.DogRecognitionModel()
        print("DogRecognition loaded successfully")
    except Exception as e:
        dog_model_init_error = str(e)
        print("DOG MODEL INIT ERROR:", e)

    return dog_model


@router.get("/dog-advice")
def dog_advice(breed: str):
    llm_instance = _get_llm()
    if llm_instance is None:
        return {"error": llm_init_error or "LLM not initialized"}

    try:
        return {"advice": llm_instance.generate_advice(breed)}
    except Exception as e:
        return {"error": str(e)}


@router.post("/dog-from-photo")
async def dog_from_photo(file: UploadFile = File(...)):
    model_instance = _get_dog_model()
    if model_instance is None:
        return {"error": dog_model_init_error or "Dog recognition model not initialized"}

    llm_instance = _get_llm()
    if llm_instance is None:
        return {"error": llm_init_error or "LLM not initialized"}

    temp_path = f"temp_{uuid.uuid4()}.jpg"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        is_dog = model_instance.is_dog(temp_path)
        if not is_dog:
            return {"error": "Sorry, this is not a dog. Please try again"}

        preds = model_instance.predict(temp_path)
        top_label = _normalize_breed_label(preds[0]["label"])

        advice = llm_instance.generate_advice(top_label)

        return {"breed": top_label, "raw_predictions": preds, "advice": advice}

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
