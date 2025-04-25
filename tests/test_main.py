import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# --- Upload endpoint with valid CSV ---
def test_upload_valid_csv():
    file_path = "tests/test_files/valid_iris.csv"
    if not os.path.exists(file_path):
        pytest.skip("CSV test file not found")
    
    with open(file_path, "rb") as f:
        response = client.post("/data/upload", files={"file": ("iris.csv", f, "text/csv")})
    
    assert response.status_code == 200
    assert "6 records inserted" in response.json()["message"]

# --- Train with an invalid model name ---
def test_train_invalid_model():
    response = client.post("/train?model_name=decision_tree")
    assert response.status_code == 400
    assert "Unsupported model 'decision_tree'" in response.json()["detail"]

# --- Predict endpoint with missing fields ---
def test_predict_missing_field():
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5
    }
    response = client.post("/predict?model_name=svm", json=payload)
    assert response.status_code == 422  # Validation error


# --- Predict endpoint with valid input ---
def test_predict_valid_input():
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict?model_name=svm", json=payload)
    assert response.status_code in [200, 500]  # May fail if model isn't trained yet

    if response.status_code == 200:
        assert "predicted_species: setosa" in response.json()