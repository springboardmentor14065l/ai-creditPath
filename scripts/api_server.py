from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import numpy as np
import os
import uvicorn
from typing import Optional, List

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(SCRIPT_DIR, '..', 'models')

app = FastAPI(
    title="CreditPathAI Risk Assessment API",
    version="1.4.1"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODEL LOADING ---
try:
    xgb_model = joblib.load(os.path.join(MODELS_DIR, 'best_xgboost_model.pkl'))
    scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.joblib'))
    EXPECTED_FEATURES = xgb_model.feature_names_in_.tolist()
    SCALED_COLS = ['income', 'loan_amount', 'credit_score', 'loan_to_income', 'credit_utilization', 
                   'interest_burden', 'employment_stability', 'log_income', 'income_loan_interaction']
    INCOME_UPPER_LIMIT = 118791.0
except Exception as e:
    print(f"Error loading models: {e}")
    raise RuntimeError("Could not load model artifacts.")

# --- DATA MODELS ---
class LoanInput(BaseModel):
    age: int
    income: float
    loan_amount: float
    credit_score: int
    months_employed: Optional[int] = 24
    num_credit_lines: Optional[int] = 3
    interest_rate: Optional[float] = 10.0
    loan_term: Optional[int] = 36
    dti_ratio: Optional[float] = 0.3
    education: Optional[str] = "Bachelor's"
    employment_type: Optional[str] = "Full-time"
    marital_status: Optional[str] = "Single"
    has_mortgage: Optional[str] = "No"
    has_dependents: Optional[str] = "No"
    loan_purpose: Optional[str] = "Other"
    has_cosigner: Optional[str] = "No"

class PredictionResponse(BaseModel):
    probability: float
    risk: str
    action: str

# --- UTILITY FUNCTIONS ---
def recommend_action(prob: float):
    # Updated Thresholds (User requested "Normal" levels)
    if prob < 0.30:
        return "Low", "Low Risk - Send Routine Reminder"
    elif prob < 0.60:
        return "Medium", "Medium Risk - Manual Review / Call Customer"
    else:
        return "High", "High Risk - Immediate Recovery Action Required"

def feature_pipeline(data: LoanInput):
    """Manual mapping for single-row inference to avoid pd.get_dummies drop_first bugs."""
    input_df = pd.DataFrame(np.zeros((1, len(EXPECTED_FEATURES))), columns=EXPECTED_FEATURES)
    
    income_capped = min(data.income, INCOME_UPPER_LIMIT)
    input_df['age'] = data.age
    input_df['income'] = income_capped
    input_df['loan_amount'] = data.loan_amount
    input_df['credit_score'] = data.credit_score
    input_df['months_employed'] = data.months_employed
    input_df['num_credit_lines'] = data.num_credit_lines
    input_df['interest_rate'] = data.interest_rate
    input_df['loan_term'] = data.loan_term
    input_df['dti_ratio'] = data.dti_ratio
    
    input_df['loan_to_income'] = data.loan_amount / max(income_capped, 1)
    input_df['credit_utilization'] = data.loan_amount / max(data.num_credit_lines, 1)
    input_df['interest_burden'] = data.loan_amount * data.interest_rate
    input_df['employment_stability'] = data.months_employed / max(data.age, 1)
    input_df['high_dti_flag'] = 1 if data.dti_ratio > 0.5 else 0
    input_df['log_income'] = np.log1p(income_capped)
    input_df['income_loan_interaction'] = income_capped * data.loan_amount

    # Categorical Mapping - Case Insensitive
    edu = str(data.education).strip().lower()
    if edu == "high school": input_df['education_High School'] = 1
    elif edu == "master's": input_df["education_Master's"] = 1
    elif edu == "phd": input_df['education_PhD'] = 1
    
    emp = str(data.employment_type).strip().lower()
    if emp == "part-time": input_df['employmenttype_Part-time'] = 1
    elif emp == "self-employed": input_df['employmenttype_Self-employed'] = 1
    elif emp == "unemployed": input_df['employmenttype_Unemployed'] = 1

    mar = str(data.marital_status).strip().lower()
    if mar == "single": input_df['maritalstatus_Single'] = 1
    elif mar == "married": input_df['maritalstatus_Married'] = 1

    if str(data.has_mortgage).strip().lower() == "yes": input_df['hasmortgage_Yes'] = 1
    if str(data.has_dependents).strip().lower() == "yes": input_df['hasdependents_Yes'] = 1
    if str(data.has_cosigner).strip().lower() == "yes": input_df['hascosigner_Yes'] = 1
    
    purpose = str(data.loan_purpose).strip().lower()
    if purpose == "business": input_df['loanpurpose_Business'] = 1
    elif purpose == "education": input_df['loanpurpose_Education'] = 1
    elif purpose == "home": input_df['loanpurpose_Home'] = 1
    elif purpose == "other": input_df['loanpurpose_Other'] = 1

    if 600 < data.credit_score <= 700: input_df['credit_score_bucket_Average'] = 1
    elif 700 < data.credit_score <= 800: input_df['credit_score_bucket_Good'] = 1
    elif data.credit_score > 800: input_df['credit_score_bucket_Excellent'] = 1

    input_df[SCALED_COLS] = scaler.transform(input_df[SCALED_COLS])
    return input_df

# --- ENDPOINTS ---
from fastapi.responses import RedirectResponse

@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')

@app.post("/predict")
def predict(data: LoanInput):
    try:
        transformed_df = feature_pipeline(data)
        prob = float(xgb_model.predict_proba(transformed_df)[0][1])
        risk_label, action_str = recommend_action(prob)
        return {
            "probability": round(prob, 2),
            "risk": risk_label,
            "action": action_str
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference Error: {str(e)}")

@app.post("/predict/batch")
def predict_batch(data_list: List[LoanInput]):
    """Batch processing for multiple loan applications."""
    results = []
    try:
        for data in data_list:
            transformed_df = feature_pipeline(data)
            prob = float(xgb_model.predict_proba(transformed_df)[0][1])
            risk_label, action_str = recommend_action(prob)
            results.append({
                "probability": round(prob, 2),
                "risk": risk_label,
                "action": action_str
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch Inference Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
