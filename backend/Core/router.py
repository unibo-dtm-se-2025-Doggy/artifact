from fastapi import APIRouter, File, UploadFile

from backend.Features.DogRecognition.dog_recognition import DogRecognitionModel
from backend.Features.LLM.llm_engine import DogLLMEngine

router = APIRouter()

ml_model = DogRecognitionModel()
llm_engine = DogLLMEngine()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    file_location = f"uploaded_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    result = ml_model.predict(file_location)
    return {"predictions": result}
