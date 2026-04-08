import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_case(name, data):
    print(f"\n--- Testing: {name} ---")
    try:
        response = requests.post(f"{BASE_URL}/predict", json=data)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}. Is the server running?")

if __name__ == "__main__":
    # Test 1: High Stability (Low Risk)
    test_case("Low Risk Profile", {
        "age": 45,
        "income": 120000,
        "loan_amount": 5000,
        "credit_score": 820
    })

    # Test 2: Borderline Case (Medium Risk)
    test_case("Medium Risk Profile", {
        "age": 25,
        "income": 30000,
        "loan_amount": 40000,
        "credit_score": 580,
        "loan_term": 60,
        "dti_ratio": 0.55
    })

    # Test 3: High Default Probability (High Risk)
    test_case("High Risk Profile", {
        "age": 19,
        "income": 12000,
        "loan_amount": 80000,
        "credit_score": 320,
        "employment_type": "Unemployed",
        "dti_ratio": 0.85
    })
