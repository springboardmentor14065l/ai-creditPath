import numpy as np   # ✅ FIRST

# ✅ DEFINE FUNCTION BEFORE LOADING
from feature_utils import feature_engineering


# 👇 THEN IMPORT EVERYTHING ELSE
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 👇 THEN LOAD PIPELINE
pipeline = joblib.load(r"C:\Users\prana\Downloads\creditpath\final_pipeline.pkl")

app = FastAPI(docs_url="/docs")

class LoanInput(BaseModel):
    age: int
    income: float
    loanamount: float
    monthly_debt: float
    creditscore: int
    interestrate: float
    monthsemployed: int
    hascosigner: str
    employmenttype: str   # "unemployed", "self-employed", "other"
    maritalstatus: str

def get_risk(prob):
    if prob < 0.3:
        return "Low"
    elif prob < 0.6:
        return "Medium"
    else:
        return "High"

def recommend_action(prob):
    if prob < 0.3:
        return "Low Risk - Send Reminder"
    elif prob < 0.6:
        return "Medium Risk - Call Customer"
    else:
        return "High Risk - Immediate Recovery Action"

@app.post("/predict")
def predict(data: LoanInput):
    # -----------------------------
    # Step 1: Convert input
    # -----------------------------
    input_dict = data.dict()
    # -----------------------------
    # Step 2: Calculate DTI
    # -----------------------------
    input_dict["dtiratio"] = input_dict["monthly_debt"] / (input_dict["income"] + 1)
    input_dict.pop("monthly_debt")
    # -----------------------------
    # Step 3: Encode categorical
    # -----------------------------
    input_dict["hascosigner_yes"] = 1 if data.hascosigner.lower() == "yes" else 0
    input_dict["employmenttype_unemployed"] = 1 if data.employmenttype == "unemployed" else 0
    input_dict["employmenttype_self-employed"] = 1 if data.employmenttype == "self-employed" else 0
    input_dict["maritalstatus_married"] = 1 if data.maritalstatus == "married" else 0
    # ❗ Remove original string columns
    input_dict.pop("hascosigner")
    input_dict.pop("employmenttype")
    input_dict.pop("maritalstatus")
    # -----------------------------
    # Step 4: Create DataFrame
    # -----------------------------
    input_df = pd.DataFrame([input_dict])
    # -----------------------------
    # Step 5: Fix column order
    # -----------------------------
    expected_order = [
        "age", "income", "loanamount", "creditscore",
        "interestrate", "monthsemployed",
        "hascosigner_yes",
        "employmenttype_unemployed",
        "employmenttype_self-employed",
        "maritalstatus_married",
        "dtiratio"
    ]
    input_df = input_df[expected_order]
    # -----------------------------
    # Step 6: Prediction
    # -----------------------------
    prob = pipeline.predict_proba(input_df)[0][1]
    return {
        "probability": float(prob),
        "risk": get_risk(prob),
        "action": recommend_action(prob)
    }

