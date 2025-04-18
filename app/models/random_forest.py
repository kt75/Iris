from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from app.models.base_model import BaseModel

class RandomForestModel(BaseModel):
    MODEL_PATH = "models/random_forest_model.pkl"

    def train(self, X, y):
        # A classification problem based on species
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        model = RandomForestClassifier(random_state=42)
        model.fit(X, y_encoded)

        self.save((model, le))
        return model, le
