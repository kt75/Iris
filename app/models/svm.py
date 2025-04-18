from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from app.models.base_model import BaseModel

class SVMModel(BaseModel):
    MODEL_PATH = "models/svm_model.pkl"

    def train(self, X, y):
        # A classification problem based on species
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # Based on visualization, data is approximately linearly seperable
        model = SVC(kernel="linear", probability=True)
        model.fit(X, y_encoded)

        self.save((model, le))
        return model, le