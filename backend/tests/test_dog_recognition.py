import os
import tempfile

from PIL import Image

import backend.Features.DogRecognition.dog_recognition as dog_recognition_module
from backend.Features.DogRecognition.dog_recognition import DogRecognitionModel


def make_temp_image():
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    Image.new("RGB", (4, 4), color=(120, 120, 120)).save(tmp.name, format="JPEG")
    return tmp.name


def test_is_dog_and_predict(monkeypatch):
    class ZeroShotStub:
        def __call__(self, images=None, candidate_labels=None):
            return [{"label": "dog"}]

    class ClassifierStub:
        def __call__(self, img):
            return [
                {"label": "husky", "score": 0.9},
                {"label": "pug", "score": 0.05},
                {"label": "cat", "score": 0.01},
                {"label": "wolf", "score": 0.01},
            ]

    def fake_pipeline(task, model=None):
        if task == "zero-shot-image-classification":
            return ZeroShotStub()
        if task == "image-classification":
            return ClassifierStub()
        raise ValueError("unexpected task")

    monkeypatch.setattr(dog_recognition_module, "pipeline", fake_pipeline)

    model = DogRecognitionModel()
    img_path = make_temp_image()

    try:
        assert model.is_dog(img_path) is True
        preds = model.predict(img_path)
        assert len(preds) == 3
        assert preds[0]["label"] == "husky"
    finally:
        os.remove(img_path)


def test_zero_shot_not_dog(monkeypatch):
    class ZeroShotStub:
        def __call__(self, images=None, candidate_labels=None):
            return [{"label": "not dog"}]

    class ClassifierStub:
        def __call__(self, img):
            return [{"label": "husky", "score": 0.5}]

    def fake_pipeline(task, model=None):
        if task == "zero-shot-image-classification":
            return ZeroShotStub()
        if task == "image-classification":
            return ClassifierStub()
        raise ValueError("unexpected task")

    monkeypatch.setattr(dog_recognition_module, "pipeline", fake_pipeline)

    model = DogRecognitionModel()
    img_path = make_temp_image()

    try:
        assert model.is_dog(img_path) is False
    finally:
        os.remove(img_path)
