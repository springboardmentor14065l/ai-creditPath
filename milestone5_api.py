from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import logging
import os
import math

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load model and pipeline
MODEL_PATH = "model.pkl"
PIPELINE_PATH = "pipeline.pkl"

try:
    model = joblib.load(MODEL_PATH)
    pipeline = joblib.load(PIPELINE_PATH)
    logger.info("Model and pipeline loaded successfully.")
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    raise HTTPException(status_code=500, detail="Model or pipeline file not found.")
except Exception as e:
    logger.error(f"Error loading model or pipeline: {e}")
    raise HTTPException(status_code=500, detail="Error loading model or pipeline.")

# Define Pydantic schema for input validation
class LoanApplication(BaseModel):
    LoanID: int
    Age: int
    LoanAmount: float
    Income: float  # Added Income field
    CreditScore: int
    MonthsEmployed: int
    NumCreditLines: int
    InterestRate: float
    LoanTerm: int
    DTIRatio: float
    Education: int
    EmploymentType: int
    MaritalStatus: int
    HasMortgage: int
    HasDependents: int
    LoanPurpose: int
    HasCoSigner: int
    loan_income_ratio: float
    credit_utilization: float
    interest_burden: float
    employment_stability: float
    high_dti_flag: int
    credit_score_Poor: int
    credit_score_Average: int
    credit_score_Good: int
    credit_score_Excellent: int
    log_income: float
    income_loan_interaction: float

# Define thresholds for risk classification
HIGH_RISK_THRESHOLD = 0.95  # Increased threshold for High Risk
MEDIUM_RISK_THRESHOLD = 0.7  # Adjusted threshold for Medium Risk

# Root endpoint
@app.get("/")
async def root():
    return {"message": "CreditPathAI API is running"}



# Prediction endpoint
@app.post("/predict")
async def predict(input_data: LoanApplication):
    try:
        # Convert input data to dictionary
        input_dict = input_data.dict()

        # Update the preprocessing logic to calculate derived features from Income
        def preprocess_input(data):
            # Calculate derived features
            data['loan_income_ratio'] = data['LoanAmount'] / data['Income']
            data['log_income'] = math.log(data['Income'])
            data['income_loan_interaction'] = data['Income'] * data['LoanAmount']

            # Set default values for one-hot encoded fields
            data['credit_score_Poor'] = 1 if data['CreditScore'] < 580 else 0
            data['credit_score_Average'] = 1 if 580 <= data['CreditScore'] < 670 else 0
            data['credit_score_Good'] = 1 if 670 <= data['CreditScore'] < 740 else 0
            data['credit_score_Excellent'] = 1 if data['CreditScore'] >= 740 else 0

            return data

        input_dict = preprocess_input(input_dict)

        # Convert to DataFrame
        input_df = pd.DataFrame([input_dict])

        # Ensure column order matches training
        expected_columns = pipeline['features']
        input_df = input_df[expected_columns]

        # Apply preprocessing pipeline
        processed_data = pipeline['scaler'].transform(input_df)

        # Get prediction probabilities
        probabilities = model.predict_proba(processed_data)[0]
        prediction_probability = probabilities[1]  # Assuming class 1 is default

        # Determine risk category
        if prediction_probability > HIGH_RISK_THRESHOLD:
            risk = "High"
            action = "High Risk - Immediate Recovery Action"
        elif prediction_probability > MEDIUM_RISK_THRESHOLD:
            risk = "Medium"
            action = "Medium Risk - Monitor Closely"
        else:
            risk = "Low"
            action = "Low Risk - Approved"

        # Return response
        return {
            "probability": prediction_probability,
            "risk": risk,
            "action": action
        }

    except KeyError as e:
        logger.error(f"Key error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input data: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")