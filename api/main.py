# api/main.py

from fastapi import FastAPI
import numpy as np
import pickle
from src.recommendation import get_recommendation

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "CreditPathAI API Running"}

@app.post("/predict")
def predict(data: dict):

    import pandas as pd

    # Convert to DataFrame (IMPORTANT)
    input_df = pd.DataFrame([data])

    # Keep only numeric columns
    input_df = input_df.select_dtypes(include=['int64','float64'])

    # Prediction
    prob = model.predict_proba(input_df)[0][1]

    recommendation = get_recommendation(prob)

    return {
        "default_probability": float(prob),
        "recommendation": recommendation
    }