import joblib
import pandas as pd
import numpy as np

# Load saved assets
try:
    model = joblib.load("model.pkl")
    pipeline = joblib.load("pipeline.pkl")
    print("✅ Assets loaded.")
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

# Sample data
data = {
    "age": 35,
    "income": 50000,
    "loan_amount": 10000,
    "credit_score": 750,
    "months_employed": 24,
    "num_credit_lines": 3,
    "interest_rate": 5.5,
    "loan_term": 12,
    "dti_ratio": 0.2,
    "education": 1,
    "employment_type": 1,
    "marital_status": 1,
    "has_mortgage": 0,
    "has_dependents": 0,
    "loan_purpose": 2,
    "has_cosigner": 0
}

df = pd.DataFrame([data])
print("Transforming...")
processed = pipeline.transform(df)
print("Predicting...")
prob = model.predict_proba(processed)[:, 1][0]
print(f"Result: {prob}")
