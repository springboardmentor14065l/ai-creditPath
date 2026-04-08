import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# --- Test Cases ---
test_cases = [
    {
        "label": "High Risk Borrower",
        "data": {
            "age": 35,
            "income": 30000,
            "loan_amount": 120000,
            "credit_score": 520,
            "months_employed": 2,
            "num_credit_lines": 3,
            "interest_rate": 22.5,
            "loan_term": 60,
            "dti_ratio": 0.85,
            "education": "High School",
            "employment_type": "Unemployed",
            "marital_status": "Single",
            "has_mortgage": "No",
            "has_dependents": "Yes",
            "loan_purpose": "Business",
            "has_cosigner": "No"
        }
    },
    {
        "label": "Medium Risk Borrower",
        "data": {
            "age": 42,
            "income": 65000,
            "loan_amount": 80000,
            "credit_score": 620,
            "months_employed": 12,
            "num_credit_lines": 5,
            "interest_rate": 14.0,
            "loan_term": 48,
            "dti_ratio": 0.52,
            "education": "Bachelor's",
            "employment_type": "Part-time",
            "marital_status": "Married",
            "has_mortgage": "Yes",
            "has_dependents": "Yes",
            "loan_purpose": "Other",
            "has_cosigner": "No"
        }
    },
    {
        "label": "Low Risk Borrower",
        "data": {
            "age": 50,
            "income": 130000,
            "loan_amount": 40000,
            "credit_score": 800,
            "months_employed": 24,
            "num_credit_lines": 8,
            "interest_rate": 5.5,
            "loan_term": 24,
            "dti_ratio": 0.2,
            "education": "Master's",
            "employment_type": "Full-time",
            "marital_status": "Married",
            "has_mortgage": "Yes",
            "has_dependents": "No",
            "loan_purpose": "Home",
            "has_cosigner": "Yes"
        }
    },
    {
        "label": "Handout Example (age=40, income=50000, loan=20000, score=620)",
        "data": {
            "age": 40,
            "income": 50000,
            "loan_amount": 20000,
            "credit_score": 620,
            "months_employed": 8,
            "num_credit_lines": 4,
            "interest_rate": 15.0,
            "loan_term": 36,
            "dti_ratio": 0.55,
            "education": "Bachelor's",
            "employment_type": "Full-time",
            "marital_status": "Single",
            "has_mortgage": "No",
            "has_dependents": "No",
            "loan_purpose": "Other",
            "has_cosigner": "No"
        }
    }
]

# --- Run Tests ---
print("=" * 60)
print("CreditPathAI API - Test Cases")
print("=" * 60)

# Health check
print("\n[Health Check]")
r = requests.get(f"{BASE_URL}/health")
print(r.json())

# Risk info
print("\n[Risk Thresholds]")
r = requests.get(f"{BASE_URL}/risk-info")
print(json.dumps(r.json(), indent=2))

# Individual predictions
print("\n[Individual Predictions]")
for tc in test_cases:
    print(f"\nTest: {tc['label']}")
    r = requests.post(f"{BASE_URL}/predict", json=tc['data'])
    result = r.json()
    print(f"  Probability : {result['probability']}")
    print(f"  Risk Level  : {result['risk']}")
    print(f"  Action      : {result['action']}")

# Batch prediction
print("\n[Batch Prediction]")
batch_payload = {"records": [tc['data'] for tc in test_cases]}
r = requests.post(f"{BASE_URL}/predict-batch", json=batch_payload)
batch_result = r.json()
print(f"Total predictions: {batch_result['total']}")
for i, pred in enumerate(batch_result['predictions']):
    print(f"  Record {i+1}: prob={pred['probability']} | risk={pred['risk']} | action={pred['action']}")

print("\n" + "=" * 60)
print("All tests passed!")
print("=" * 60)
