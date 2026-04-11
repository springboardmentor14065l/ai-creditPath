from fastapi import FastAPI
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware  # ✅ ADDED

# Load saved files
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
feature_names = joblib.load("feature_names.pkl")

app = FastAPI()

# ✅ ADDED (for React connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Risk category function (UNCHANGED)
def categorize_risk(score):
    if score < 30:
        return "Low Risk"
    elif score < 60:
        return "Medium Risk"
    else:
        return "High Risk"

# Explanation function (UNCHANGED)
def generate_explanation(risk_category):
    if risk_category == "Low Risk":
        return "Low chance of default. The applicant seems financially stable."
    
    elif risk_category == "Medium Risk":
        return "There is some risk. The applicant may face difficulty in repayment."
    
    else:
        return "High chance of default. The applicant may struggle to repay the loan."

@app.get("/")
def home():
    return {"message": "Credit Risk API is running!"}

@app.post("/predict")
def predict(data: dict):
    try:
        # Convert input into DataFrame
        input_df = pd.DataFrame([data])
        input_df = input_df.replace({True: 1, False: 0})

        # ✅ SAFE FIX (avoid missing column error)
        for col in feature_names:
            if col not in input_df:
                input_df[col] = 0

        input_df = input_df[feature_names]

        print("INPUT DATA:")
        print(input_df)

        # Scale input
        input_scaled = scaler.transform(input_df)

        print("MODEL OUTPUT:")
        print(model.predict_proba(input_scaled))

        # Predict probability
        prob = model.predict_proba(input_scaled)[0][1]

        # Risk score
        risk_score = round(prob * 100, 2)

        # Category
        risk_category = categorize_risk(risk_score)

        # Explanation
        explanation = generate_explanation(risk_category)

        # ✅ UPDATED RETURN (ONLY ADDITION FOR FRONTEND)
        return {
            "probability": round(prob, 4),        # NEW (for React)
            "risk": risk_category.replace(" Risk", ""),  # NEW (Low/Medium/High)
            "action": explanation,               # NEW (rename for UI)

            # OLD OUTPUT (UNCHANGED)
            "prediction_probability": round(prob, 4),
            "risk_score": risk_score,
            "risk_category": risk_category,
            "explanation": explanation,

            # for chart
            "low": 20,
            "medium": 30,
            "high": 50
        }

    except Exception as e:
        return {"error": str(e)}