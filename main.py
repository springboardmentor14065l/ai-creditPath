from fastapi import FastAPI
import pandas as pd
import joblib

# Load saved files
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
feature_names = joblib.load("feature_names.pkl")

app = FastAPI()

# Risk category function
def categorize_risk(score):
    if score < 30:
        return "Low Risk"
    elif score < 60:
        return "Medium Risk"
    else:
        return "High Risk"
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

        # Ensure correct feature order
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

        # ✅ ADD THIS LINE
        explanation = generate_explanation(risk_category)

        # ✅ UPDATED RETURN BLOCK
        return {
            "prediction_probability": round(prob, 4),
            "risk_score": risk_score,
            "risk_category": risk_category,
            "explanation": explanation
        }

    except Exception as e:
        return {"error": str(e)}