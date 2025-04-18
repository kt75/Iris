from fastapi import FastAPI, HTTPException, Body, UploadFile, File, Query
from app import mongodb
from app.models.logistic_regression import LogisticModel
from app.models.random_forest import RandomForestModel
from app.models.svm import SVMModel
from app.iris import IrisSample, IrisInput
from app import utils

app = FastAPI()


@app.post("/data")
def add_sample(sample: IrisSample):
    # Add one iris_sample based on the Iris class
    try:
        mongodb.insert_sample(sample)
    except Exception as e:
        print("Error: ", e)
        raise Exception("Database insert failed")
    return {"message": "Sample added"}

@app.post("/data/upload")
def upload_samples(file: UploadFile = File(...)):
    # Load the dataset (CSV File only) and add the content to MongoDB
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    records,error=utils.process_csv(file)
    if error:
       raise HTTPException(status_code=400, detail=error)

    try:
        print(records[0])
        print(len(records))
        mongodb.insert_samples(records)
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail="Failed to save data")
    
    return {"message": f"{len(records)} records inserted"}


@app.get("/data")
def get_samples(species: str = None):
    # Filter on species column
    try:
        samples = mongodb.get_samples(species)
        return samples
    except Exception as e:
        print("Error: ", e) 
        raise HTTPException(status_code=500, detail="Failed to fetch data from database")


TRAIN_MODEL = {
    "svm": SVMModel,
    "logistic": LogisticModel,
    "random_forest": RandomForestModel,
}

@app.post("/train")
def train_model(model_name: str = Query(..., description="Model to train: svm, logistic, random_forest")):
    # SPLIT DATA
    X_train, X_test, y_train, y_test=utils.split_data()
    if not X_train:
        raise HTTPException(status_code=400, detail="No data to train on")
    if model_name not in TRAIN_MODEL:
        raise HTTPException(status_code=400, detail=f"Unsupported model '{model_name}'")
    
    model_class = TRAIN_MODEL[model_name]()
    model, le = model_class.train(X_train, y_train)
    accuracy = model_class.evaluate(model, X_test, y_test, label_encoder=le)

    return {"message": "Model trained and saved successfully.",
            "accuracy": round(accuracy, 4)}


@app.post("/predict")
def predict(input: IrisInput, model_name: str = Query(..., description="Model to use: svm, logistic, random_forest")):
    if model_name not in TRAIN_MODEL:
        raise HTTPException(status_code=400, detail=f"Unsupported model '{model_name}'")

    model = TRAIN_MODEL[model_name]()
    try:
        prediction = model.predict(input.to_feature_list())
    except Exception:
        raise HTTPException(status_code=500, detail="Prediction failed")
    
    return {"predicted_species": prediction}