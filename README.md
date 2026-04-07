# CreditPathAI - Milestone 5: Recommendation Engine & FastAPI API

Welcome to **Milestone 5** of the CreditPathAI project! This milestone focuses on taking the trained machine learning models from Milestone 4 and deploying them as a production-ready API with an automated business recommendation engine.

## 🚀 Overview

In this phase, we have integrated our advanced XGBoost model into a **FastAPI** web application. The API accepts loan application data, processes it using the exact same feature engineering logic used during training, and returns a risk assessment along with a recommended action.

## 🛠️ Key Features

- **Standardized Preprocessing**: Reuses the Milestone 4 preprocessing logic (scaling, encoding, and 10+ custom feature transformations) via a serialized scikit-learn `Pipeline`.
- **FastAPI Integration**: High-performance, asynchronous API with automatic interactive documentation (Swagger UI).
- **Automated Recommendation Engine**: Translates complex machine learning probabilities into clear business strategies.
- **Robust Error Handling**: Handles edge cases like zero values or missing inputs without crashing.

## 📂 Project Structure

- `main.py`: The core FastAPI application.
- `utils.py`: Contains the `feature_engineering` function shared between training and inference.
- `advanced_model_training.py`: Updated training script that exports `model.pkl` and `pipeline.pkl`.
- `model.pkl`: The trained XGBoost model.
- `pipeline.pkl`: The saved preprocessing pipeline.

## ⚙️ Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn pandas numpy scikit-learn xgboost joblib
   ```

2. **Generate Assets** (if not already present):
   ```bash
   python advanced_model_training.py
   ```

3. **Run the API**:
   ```bash
   uvicorn main:app --reload
   ```

## 📡 API Documentation

Once the server is running, you can access the interactive documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoint: `POST /predict`

**Request Body (JSON):**
```json
{
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
```

**Response (JSON):**
```json
{
  "probability": 0.2752,
  "risk": "Low Risk",
  "action": "Send Reminder"
}
```

## ⚖️ Recommendation Logic

The recommendation engine categorizes applications based on the predicted probability of default:

| Probability Stage | Risk Category | Recommended Action |
| :--- | :--- | :--- |
| **Prob < 0.3** | Low Risk | **Send Reminder** |
| **0.3 ≤ Prob < 0.6** | Medium Risk | **Call Customer** |
| **Prob ≥ 0.6** | High Risk | **Immediate Recovery Action** |

---
*Developed as part of the CreditPathAI Project.*
