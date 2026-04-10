# CreditPathAI

Welcome to **CreditPathAI**, a complete end-to-end, full-stack application designed to predict the probability of loan defaults using advanced machine learning models (XGBoost & LightGBM) and a modern, high-performance web interface.

![Project Status](https://img.shields.io/badge/Status-Complete-success) ![Machine Learning](https://img.shields.io/badge/ML-XGBoost%20%7C%20LightGBM-blue) ![Backend](https://img.shields.io/badge/Backend-FastAPI-009688) ![Frontend](https://img.shields.io/badge/Frontend-React%20%7C%20Vite%20%7C%20Tailwind-61DAFB)

---

## 🚀 Overview
CreditPathAI unifies data science and full-stack engineering. The application takes in a borrower's demographic and financial profile and provides a robust, ML-driven risk assessment via an immersive dashboard. 

The project comprises:
1. **Machine Learning Pipeline**: Data preprocessing, feature engineering, class-imbalance correction, and sophisticated modeling utilizing gradient boosting.
2. **FastAPI Backend Engine**: A low-latency, scalable Python API wrapper running the serialized ML model pipeline.
3. **React/Vite Dashboard**: A dynamic, beautiful front-end displaying real-time Probability Gauges, Custom KPIs, Risk Insights, and historical tracking.

---

## 🛠️ Key Features

### 🧠 Advanced Machine Learning
- **Gradient Boosting Frameworks**: Leverages tuned `XGBClassifier` and `LGBMClassifier` architectures.
- **Automated Feature Engineering**: Handles over 10+ synthesized metrics (like `monthly_interest_burden`) mapped via scikit-learn `FunctionTransformer` Pipelines.
- **Native Threshold Calibration**: Probability output bounds are mathematically calibrated and offset to properly adjust for heavily skewed target class ratios inherent in real-life debt data.

### ⚙️ FastAPI Python Backend
- **Asynchronous endpoints**: Highly responsive asynchronous architecture.
- **Smart Decision Engine**: Uses calibrated bounds mapping default probabilities securely to three business actions:
  - `< 0.25`: **Low Risk** _(Regular follow-up)_
  - `0.25 - 0.40`: **Medium Risk** _(Send reminder and monitor)_
  - `≥ 0.40`: **High Risk** _(Immediate call and restructuring plan)_

### 🖥️ Dynamic React Interface
- **KPI Metrics Navbar**: Tracks session counts and sums aggregated predictions seamlessly across browser sessions via `localStorage`.
- **Interactive Risk Results**: Contextual UI components that animate and change tone (Green / Amber / Red) reacting precisely to the AI engine predictions.
- **Embedded Visualizations**: Native Plotly.js charts displaying real-time gauges.

---

## 📂 Architecture & Project Structure

```text
creditpathai/
│
├── frontend/                   # React.js application
│   ├── src/                    # Source code (React components, hooks, api)
│   ├── index.html              # Vite Entry Point
│   ├── vite.config.js          # Vite Bundler Settings
│   └── package.json            # Node Dependencies
│
├── main.py                     # Core FastAPI Application & Routing
├── utils.py                    # Feature Engineering Functions
├── advanced_model_training.py  # Model Logic & Training Architecture
├── eda_analysis.py             # Exploratory Data Analytics Logic
├── model.pkl                   # Serialized XGBoost Predictor
├── pipeline.pkl                # Serialized Data Transformation Pipeline
└── README.md                   # Project Documentation
```

---

## ⚙️ Installation & Usage Guide

### 1. Backend Setup (FastAPI & ML)
Ensure you have Python 3.9+ installed natively or mapped in your virtual environment.

```bash
# Navigate to project root
cd creditpathai

# Install dependencies
pip install fastapi uvicorn pandas numpy scikit-learn xgboost lightgbm joblib

# (Optional) Verify & Retrain the assets if desired
python advanced_model_training.py

# Launch the FastAPI Uvicorn Server (Default Port: 8000)
python main.py
```

### 2. Frontend Setup (React & Vite)
Ensure you have Node.js v16+ installed. Open a second terminal window.

```bash
# Navigate to the frontend directory
cd creditpathai/frontend

# Install dependencies Node Modules
npm install

# Start the Vite local development server (Port 5173/5174)
npm run dev
```

### 3. Execution
1. The **Backend API** will host the documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
2. Open your web browser to **[http://localhost:5173/](http://localhost:5173/)** (check the Vite output if using 5174).
3. Utilize the Form on the left side of the dashboard. Click **Predict Risk** to trigger the full execution pipeline.

---

## 📡 API Reference Endpoint

### `POST /predict`
Processes applicant data and outputs the risk probability and recommended administrative action.

**Example Request:**
```json
{
  "age": 35,
  "income": 50000,
  "loan_amount": 10000,
  "credit_score": 750,
  "months_employed": 24,
  "num_credit_lines": 3,
  "interest_rate": 5.5,
  "loan_term": 36,
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

**Example Response:**
```json
{
  "probability": 0.2752,
  "risk": "Medium Risk",
  "action": "Send reminder and monitor"
}
```

---
*Created as the final milestone of the CreditPathAI Risk Assessment project.*
