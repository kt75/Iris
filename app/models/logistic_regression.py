from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from app.models.base_model import BaseModel

class LogisticModel(BaseModel):
    MODEL_PATH = "models/logistic_model.pkl"

    def train(self, X, y):
        # A classification problem based on species
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # Multi-Class Classification Problem, 
        model = LogisticRegression(multi_class='multinomial')
        model.fit(X, y_encoded)

        self.save((model, le))
        return model, le
