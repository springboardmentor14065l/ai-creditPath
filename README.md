# CreditPathAI

Automating and Optimizing the Loan Recovery Lifecycle

---

## Overview

CreditPathAI is a machine learningâ€“driven platform designed to automate and optimize the loan recovery lifecycle by modeling borrower repayment behavior and predicting default risk.

The system uses open-source technologies to build a scalable, cost-effective, and production-ready solution that enables financial institutions to improve delinquency recovery efficiency and equip collection agents with actionable insights.

---

## Project Objective

The objective of this project is to design and develop a predictive analytics platform that:

* Predicts borrower default probability
* Segments borrowers based on risk level
* Recommends personalized recovery strategies
* Improves recovery efficiency across loan portfolios
* Supports data-driven decision-making

---

## Dataset

This project uses the **Default of Credit Card Clients Dataset (Taiwan)**.

* Approximately 30,000 borrower records
* 25 financial and demographic features
* Binary target variable: `default.payment.next.month`

The dataset includes:

* Credit limit
* Repayment status for six months
* Billing amounts for six months
* Payment amounts for six months
* Demographic attributes

This dataset enables modeling of repayment behavior and credit risk patterns.

---

## Project Architecture

The system is structured into the following layers:

1. Data Ingestion Layer
2. Feature Engineering Pipeline
3. Model Training and Evaluation
4. Recommendation Engine
5. API Serving Layer
6. Visualization Dashboard

---

## Tech Stack

### Data Processing

* Python
* Pandas
* NumPy
* SQLite / PostgreSQL

### Machine Learning

* scikit-learn
* Logistic Regression (baseline)
* XGBoost
* LightGBM
* MLflow (experiment tracking)

### Backend

* FastAPI
* Docker

### Frontend

* React.js
* Plotly.js

---

## Model Development Strategy

### Baseline Model

Logistic Regression to establish benchmark performance.

### Advanced Models

* XGBoost
* LightGBM

### Evaluation Metrics

* AUC-ROC
* Confusion Matrix
* Precision / Recall
* F1 Score

---

## Risk Segmentation Strategy

Borrowers are categorized based on predicted probability:

* Low Risk
* Medium Risk
* High Risk

Each risk category is mapped to a personalized recovery action through the recommendation engine.

---

## Repository Structure
```
ai-creditPath/
â”œâ”€â”€ Loan_Default.csv
â”œâ”€â”€ clean_loans.csv
â”œâ”€â”€ import_data.py
â”œâ”€â”€ load_data.py
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md
```
---

## Future Enhancements

* SHAP-based model explainability
* Real-time scoring pipeline
* Portfolio-level risk analytics
* Automated retraining pipeline
* Cloud deployment

---

## Status

Milestone 6 delivered with a React command-center frontend, FastAPI integration, explainable prediction views, and agent-facing batch dashboards.

---

## Milestone 5: Recommendation Engine & API Prototype

This milestone converts model probabilities into business-ready actions and exposes them through a FastAPI service.

### What was delivered

* Rule-based recommendation engine:
  * `probability < 0.30` -> `Low Risk - Send Reminder`
  * `0.30 <= probability < 0.60` -> `Medium Risk - Call Customer`
  * `probability >= 0.60` -> `High Risk - Immediate Recovery Action`
* FastAPI prototype with:
  * `GET /health`
  * `POST /predict`
  * `POST /predict/batch`
* Consistent inference pipeline that:
  * rebuilds engineered features from raw borrower input
  * aligns feature order with the saved scaler and logistic model
  * applies the same scaling used during training
* Local automated tests covering:
  * single prediction
  * batch prioritization
  * validation failure handling

### Unique features added

To make CreditPathAI stand out, the API now includes two extra capabilities:

* Explainable risk drivers:
  * every prediction returns the top features pushing risk up or down
  * this helps collection agents understand why a borrower is high-risk
* Batch prioritization for operations teams:
  * `POST /predict/batch` ranks borrowers by predicted risk
  * this is useful for dashboards, call queues, and daily recovery planning

### API run command

```bash
uvicorn main:app --reload
```

Open the interactive documentation at:

`http://127.0.0.1:8000/docs`

### Example request

```json
{
  "borrower_id": "demo-1",
  "year": 2024,
  "loan_amount": 20000,
  "rate_of_interest": 0.09,
  "Interest_rate_spread": 0.02,
  "Upfront_charges": 1200,
  "term": 360,
  "property_value": 250000,
  "income": 50000,
  "Credit_Score": 620,
  "LTV": 82,
  "dtir1": 38,
  "Gender_Male": 1,
  "occupancy_type_pr": 1,
  "credit_type_EXP": 1,
  "submission_of_application_to_inst": 1
}
```

Most one-hot encoded flags are optional and default to `0`, which keeps the API easier to use while still matching the saved training contract.

### Example response

```json
{
  "probability": 1.0,
  "risk": "High",
  "action": "High Risk - Immediate Recovery Action",
  "urgency_window_hours": 4,
  "top_risk_drivers": [
    {
      "feature": "rate_of_interest",
      "label": "Interest rate",
      "raw_value": 0.09,
      "direction": "raises risk",
      "contribution": 5.2616
    }
  ]
}
```

### Local verification

The API was verified locally with:

```bash
python -m unittest discover -s tests -v
```

This confirmed:

* API health endpoint responds successfully
* `/predict` returns probability, risk, action, urgency, and explainability
* `/predict/batch` ranks borrowers correctly
* validation rejects invalid inputs such as out-of-range credit scores

---

## Milestone 6: Frontend Development and Final Delivery

Milestone 6 delivers a production-style React dashboard integrated with FastAPI for prediction, agent actions, and stakeholder validation.

### Frontend deliverables

* React.js frontend with reusable components:
  * `Dashboard.js`
  * `Form.js`
  * `Charts.js`
  * `BatchDashboard.js`
* Agent recommendation dashboard with priority ranking table
* Axios integration with:
  * `POST /predict`
  * `POST /predict/batch`
  * `GET /health`
* Plotly.js dynamic bar chart for risk distribution:
  * `Low / Medium / High` counts
  * data sourced from live API responses, not static values
* Documentation and rollout plan

### Frontend structure

```text
frontend/
+-- public/
¦   +-- index.html
+-- src/
¦   +-- components/
¦   ¦   +-- BatchDashboard.js
¦   ¦   +-- Charts.js
¦   ¦   +-- Dashboard.js
¦   ¦   +-- Form.js
¦   ¦   +-- HeroScene.js
¦   +-- data/
¦   ¦   +-- presets.js
¦   +-- services/
¦   ¦   +-- api.js
¦   +-- App.js
¦   +-- index.js
¦   +-- styles.css
+-- package.json
```

### How to run the full system

Backend:

```bash
uvicorn main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm start
```

Open the dashboard at:

`http://localhost:3000`

### UAT checklist

1. Submit a low-risk borrower and verify response fields render correctly:
   * probability
   * risk
   * action
2. Submit a high-risk borrower and verify recommendation and urgency are updated.
3. Add borrowers to queue and run batch scoring.
4. Confirm ranking is sorted by probability descending.
5. Confirm bar chart updates based on real API output.
6. Confirm validation or connectivity errors show readable messages in UI.

### Rollout plan

1. Deploy FastAPI service and verify `/health`, `/predict`, and `/predict/batch`.
2. Configure frontend API URL with `REACT_APP_API_BASE_URL`.
3. Build frontend with `npm run build` and deploy static assets.
4. Execute UAT checklist with stakeholders.
5. Capture sign-off on recommendation correctness and dashboard usability.
