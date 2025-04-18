from pydantic import BaseModel
from pydantic.dataclasses import dataclass

# Full structure for training
@dataclass
class IrisSample:
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    species: str

    FEATURE_KEYS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    LABEL_KEY = "species"

    @staticmethod
    def extract_features(samples: list) -> list:
        return [[s[k] for k in IrisSample.FEATURE_KEYS] for s in samples]
    
    @staticmethod
    def extract_labels(samples: list) -> list:
        return [s[IrisSample.LABEL_KEY] for s in samples]
    

# Subset for prediction
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    def to_feature_list(self) -> list[float]:
        return [
            self.sepal_length,
            self.sepal_width,
            self.petal_length,
            self.petal_width
        ]