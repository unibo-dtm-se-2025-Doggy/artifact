from typing import Any, Protocol


class IDogRecognitionModel(Protocol):
    def is_dog(self, image_path: str) -> bool: ...

    def predict(self, image_path: str) -> list[dict[str, Any]]: ...


class IDogLLMEngine(Protocol):
    def generate_advice(self, breed: str) -> str: ...
