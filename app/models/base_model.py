from abc import ABC, abstractmethod
import os
import pickle
from sklearn.metrics import accuracy_score

class BaseModel(ABC):
    MODEL_PATH: str

    @abstractmethod
    def train(self, X: list, y: list):
        pass

    # save pickle file 
    def save(self, model_object):
        os.makedirs(os.path.dirname(self.MODEL_PATH), exist_ok=True)
        with open(self.MODEL_PATH, "wb") as f:
            pickle.dump(model_object, f)

    # Evaluation metric: Accuracy
    def evaluate(self, model, X_test, y_test, label_encoder=None) -> float:
        y_pred = model.predict(X_test)
        if label_encoder:
            y_test = label_encoder.transform(y_test)
        acc = accuracy_score(y_test, y_pred)
        return acc
    
    def predict(self, features: list[float]) -> str:
        with open(self.MODEL_PATH, "rb") as f:
            model, le = pickle.load(f)
        label = model.predict([features])[0]
        return le.inverse_transform([label])[0]