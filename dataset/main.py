import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# --- App Setup ---
app = FastAPI(
    title="CreditPathAI API",
    description="Loan Default Prediction and Recovery Recommendation Engine",
    version="1.0.0"
)

# --- Load Model and Artifacts ---
model = joblib.load('model.pkl')
feature_columns = joblib.load('feature_columns.pkl')

# --- Input Schema ---
class LoanInput(BaseModel):
    age: int
    income: float
    loan_amount: float
    credit_score: int
    months_employed: int
    num_credit_lines: int
    interest_rate: float
    loan_term: int
    dti_ratio: float
    education: str
    employment_type: str
    marital_status: str
    has_mortgage: str
    has_dependents: str
    loan_purpose: str
    has_cosigner: str

# --- Recommendation Engine ---
def recommend_action(prob: float) -> str:
    if prob < 0.3:
        return "Low Risk - Send Reminder"
    elif prob < 0.6:
        return "Medium Risk - Call Customer"
    else:
        return "High Risk - Immediate Recovery Action"

def get_risk_level(prob: float) -> str:
    if prob < 0.3:
        return "Low"
    elif prob < 0.6:
        return "Medium"
    else:
        return "High"

# --- Feature Engineering (must match training pipeline) ---
def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:

    # Derived features
    df['loan_income_ratio']       = df['loan_amount'] / df['income']
    df['credit_utilization']      = df['loan_amount'] / df['num_credit_lines'].replace(0, 1)
    df['interest_burden']         = df['loan_amount'] * df['interest_rate']
    df['employment_stability']    = df['months_employed'] / df['age'].replace(0, 1)
    df['high_dti_flag']           = (df['dti_ratio'] > 0.5).astype(int)
    df['log_income']              = np.log1p(df['income'])
    df['income_loan_interaction'] = df['income'] * df['loan_amount']

    # Credit score bucketing
    df['credit_score_bucket'] = pd.cut(
        df['credit_score'],
        bins=[0, 600, 700, 800, 900],
        labels=['Poor', 'Average', 'Good', 'Excellent']
    )
    df = pd.get_dummies(df, columns=['credit_score_bucket'], drop_first=False)

    # Encode categoricals
    cat_cols = ['education', 'employment_type', 'marital_status', 'loan_purpose']
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    # Binary encode
    binary_cols = ['has_mortgage', 'has_dependents', 'has_cosigner']
    for col in binary_cols:
        df[col] = df[col].map({'Yes': 1, 'No': 0}).fillna(0).astype(int)

    # Drop raw income
    df.drop(columns=['income'], errors='ignore', inplace=True)

    # Align columns to training feature set
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]

    return df

# --- Root Endpoint ---
@app.get("/")
def root():
    return {
        "message": "CreditPathAI API is running",
        "docs": "http://127.0.0.1:8000/docs",
        "endpoints": ["/predict", "/health", "/risk-info"]
    }

# --- Health Check ---
@app.get("/health")
def health():
    return {"status": "healthy", "model": "XGBoost", "version": "1.0.0"}

# --- Risk Info ---
@app.get("/risk-info")
def risk_info():
    return {
        "thresholds": {
            "Low Risk":    "probability < 0.3  -> Send Reminder",
            "Medium Risk": "0.3 <= probability < 0.6  -> Call Customer",
            "High Risk":   "probability >= 0.6  -> Immediate Recovery Action"
        }
    }

# --- Predict Endpoint ---
@app.post("/predict")
def predict(data: LoanInput):
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([data.model_dump()])

        # Apply feature engineering
        input_df = apply_feature_engineering(input_df)

        # Predict probability
        prob = model.predict_proba(input_df)[0][1]

        action     = recommend_action(prob)
        risk_level = get_risk_level(prob)

        return {
            "probability": round(float(prob), 4),
            "risk":        risk_level,
            "action":      action
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Batch Predict Endpoint ---
class BatchInput(BaseModel):
    records: list[LoanInput]

@app.post("/predict-batch")
def predict_batch(data: BatchInput):
    try:
        results = []
        for record in data.records:
            input_df = pd.DataFrame([record.model_dump()])
            input_df = apply_feature_engineering(input_df)
            prob = model.predict_proba(input_df)[0][1]
            results.append({
                "probability": round(float(prob), 4),
                "risk":        get_risk_level(prob),
                "action":      recommend_action(prob)
            })
        return {"predictions": results, "total": len(results)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
