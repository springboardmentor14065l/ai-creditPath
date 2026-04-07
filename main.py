from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import uvicorn
from utils import feature_engineering

# Initialize FastAPI app
app = FastAPI(title="CreditPathAI - Loan Default Prediction API")

# Load saved assets
try:
    model = joblib.load("model.pkl")
    pipeline = joblib.load("pipeline.pkl")
    print("✅ Model and Pipeline loaded successfully!")
except Exception as e:
    print(f"❌ Error loading assets: {e}")

# Define Input Schema based on raw features
class LoanRequest(BaseModel):
    age: int
    income: float
    loan_amount: float
    credit_score: int
    months_employed: int
    num_credit_lines: int
    interest_rate: float
    loan_term: int
    dti_ratio: float
    education: int
    employment_type: int
    marital_status: int
    has_mortgage: int
    has_dependents: int
    loan_purpose: int
    has_cosigner: int

@app.get("/")
def home():
    return {"message": "Welcome to CreditPathAI Prediction API"}

@app.post("/predict")
def predict(request: LoanRequest):
    try:
        # 1. Convert request to DataFrame
        input_data = pd.DataFrame([request.dict()])
        
        # 2. Apply Pipeline (Engineering + Scaling)
        # The pipeline handles all feature engineering steps automatically
        processed_data = pipeline.transform(input_data)
        
        # 3. Predict Probability
        probability = float(model.predict_proba(processed_data)[:, 1][0])
        
        # 4. Determine Risk and Action
        if probability < 0.3:
            risk = "Low Risk"
            action = "Send Reminder"
        elif 0.3 <= probability < 0.6:
            risk = "Medium Risk"
            action = "Call Customer"
        else:
            risk = "High Risk"
            action = "Immediate Recovery Action"
        
        # 5. Return JSON Response
        return {
            "probability": round(probability, 4),
            "risk": risk,
            "action": action
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
