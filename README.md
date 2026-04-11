# CreditPath AI: End-to-End Risk Assessment System

CreditPath AI is a production-ready credit risk engine that transforms raw loan data into actionable business intelligence. It features a high-performance XGBoost model, a FastAPI backend, and an interactive React dashboard.

## 🚀 System Architecture
**Data Layer:** PostgreSQL (Local Instance)  
**Model Layer:** Tuned XGBoost (AUC 0.76)  
**API Layer:** FastAPI (Python)  
**UI Layer:** React + Axios + Plotly.js

---

## 🛠️ Setup Guide

### 1. Backend Setup
Ensure PostgreSQL is running and you have the required dependencies:
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the API Server
uvicorn scripts.api_server:app --reload
```

### 2. Frontend Setup
Navigate to the frontend directory and install dependencies:
```bash
cd frontend
npm install
npm start
```

---

## 🔌 API Endpoints

### `POST /predict`
Performs real-time risk assessment for a single loan application.
**Request Body:**
```json
{
  "age": 30, "income": 50000, "loan_amount": 20000, "credit_score": 650,
  "months_employed": 24, "num_credit_lines": 5, "interest_rate": 12.5,
  "loan_term": 36, "dti_ratio": 0.35, "education": "Bachelor's",
  "employment_type": "Full-time", "marital_status": "Single",
  "has_mortgage": "No", "has_dependents": "No", "loan_purpose": "Other", "has_cosigner": "No"
}
```

### `POST /predict/batch`
Processes multiple loan applications in a single high-concurrency request.

---

## 🖥️ Demo Explanation

The **Recovery Action Center** dashboard provides a visual interface for collection agents:

1.  **Applicant Details:** A 15-field modular form for inputting borrower data.
2.  **Visual Risk Gauge:** An interactive Plotly chart that visualizes default probability (0-100%).
3.  **Action Center:**
    *   🟢 **Low Risk (< 0.30):** Recommends "Send Routine Reminder".
    *   🟡 **Medium Risk (0.30 - 0.60):** Recommends "Manual Review / Call Customer".
    *   🔴 **High Risk (>= 0.60):** Recommends "Immediate Recovery Action" with a pulsing alert animation.
4.  **Session Analytics:** A live bar chart tracking the distribution of risk levels processed during the current session.

---

## 🛡️ Business Logic
The system is built on **Model-Action Parity**. Every prediction is calculated through the exact same 10-step feature engineering pipeline used during training, ensuring that the decisions made in the UI are mathematically identical to the historical data analysis.
