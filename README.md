# 🚀 CreditPathAI

### Intelligent Credit Risk Assessment & Decision Support System

---

## 📌 Project Overview

**CreditPathAI** is a full-stack, AI-driven application designed to evaluate customer creditworthiness using machine learning. The system predicts the **probability of default**, categorizes users into risk segments, and provides **actionable financial recommendations**.

This project simulates a **real-world fintech solution**, bridging the gap between **data science models and business decision systems**.

---

## 🎯 Key Objectives

* Build an end-to-end ML-powered credit evaluation system
* Convert raw customer data into meaningful risk insights
* Provide interpretable predictions for decision-making
* Develop a scalable and production-like architecture

---

## 🧠 System Architecture

User → React UI → Axios → FastAPI → ML Pipeline → Risk Engine → Recommendation System → JSON Response → UI

---

## 🏗️ Architecture Breakdown

### 🔹 Frontend Layer

* Built using **React.js**
* Handles user input and displays predictions
* Provides visual insights via charts

### 🔹 API Layer

* Developed using **FastAPI**
* Exposes REST endpoints for predictions
* Handles request validation and response formatting

### 🔹 Machine Learning Layer

* Preprocessing pipeline using feature engineering
* Model trained on structured financial dataset
* Outputs probability scores

### 🔹 Business Logic Layer

* Converts probability → risk category
* Generates recommendations based on risk

---

## ⚙️ Tech Stack

| Layer     | Technology              |
| --------- | ----------------------- |
| Frontend  | React.js, Axios, Plotly |
| Backend   | FastAPI, Python         |
| ML        | Scikit-learn            |
| Data      | Pandas, NumPy           |
| Dev Tools | Git, GitHub, VS Code    |

---


## 📊 Core Features

### 🔍 Credit Risk Prediction

* Predicts probability of default using ML model

### ⚠️ Risk Categorization

* Low Risk
* Medium Risk
* High Risk

### 💡 Recommendation Engine

* Suggests actions:

  * Approve loan
  * Review application
  * Reject application

### 📈 Interactive Dashboard

* Displays:

  * Probability score
  * Risk level
  * Actionable insights
* Uses Plotly for visualization

---

## 🧪 Machine Learning Workflow

1. Data Cleaning & Preprocessing
2. Feature Encoding & Transformation
3. Feature Engineering
4. Model Training (Gradient Boosting / Logistic Regression)
5. Model Evaluation (ROC-AUC, Accuracy)
6. Pipeline Creation
7. Deployment via FastAPI

---

## 📐 Risk Calculation Logic

* Model outputs probability score
* Threshold-based classification:

  * `0.0 – 0.4 → Low Risk`
  * `0.4 – 0.7 → Medium Risk`
  * `0.7 – 1.0 → High Risk`

---

## 🔗 API Documentation

### Endpoint: `POST /predict`

#### Request Example:

```json
{
  "income": 50000,
  "loan_amount": 20000,
  "credit_score": 650
}
```

#### Response Example:

```json
{
  "probability": 0.78,
  "risk": "High",
  "action": "Reject or review application"
}
```

---

## 🖥️ Frontend Capabilities

* Dynamic form-based input
* Real-time API integration
* Risk-based color coding:

  * 🔴 High Risk
  * 🟡 Medium Risk
  * 🟢 Low Risk
* Interactive charts
* Clean and responsive UI
*  💻 Frontend (Local): http://localhost:5173

---



## 🧪 Testing & Validation

* Tested with multiple input scenarios
* Verified consistency between backend and UI
* Checked edge cases for prediction stability

---

## ⚠️ Challenges Faced

* Data preprocessing complexity
* API integration issues
* Handling async calls in frontend
* Ensuring consistent data flow

---

## 🚀 Future Enhancements

* Model explainability (SHAP, LIME)
* Authentication & user management
* Cloud deployment (AWS / GCP)
* Real-time credit scoring system
* Advanced analytics dashboard

---

## 📈 Business Impact

* Helps financial institutions reduce risk
* Improves loan approval efficiency
* Provides data-driven decision support

---

## 🌟 Conclusion

CreditPathAI demonstrates how machine learning can be transformed into a **real-world decision-making system**, combining **data science, backend APIs, and frontend dashboards** into a unified application.

---
