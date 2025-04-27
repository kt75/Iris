from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://mongo:27017"))
db = client.ml_db
collection = db.iris_samples

def insert_sample(sample):
    try:
        db.iris_samples.insert_one(sample)
    except Exception as e:
        print("Error: ",e)
        raise Exception("Failed to insert data into database")

def insert_samples(samples):
    try:
        if samples:
            db.iris_samples.insert_many(samples, ordered=False)
    except Exception as e:
        print("Error: ",e)
        raise Exception("Failed to insert data into database")
    
def get_samples(species=None):
    query = {"species": species} if species else {}
    try:
        results = list(db.iris_samples.find(query, {"_id": 0}))
        return list(results)
    except Exception as e:
        print("Error: ",e)
        raise Exception("Database query failed")

def remove_samples():
    try:
        db.iris_samples.delete_many({})
    except Exception as e:
        print("Error: ",e)
        raise Exception("Failed to remove data")