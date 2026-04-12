# ai-creditPath

CreditPathAI – Loan Risk Prediction System
 A full-stack machine learning application that predicts loan default risk and provides actionable insights using a modern banking-style dashboard.

Overview

CreditPathAI is an end-to-end AI-powered system designed to assist financial institutions in evaluating borrower risk. It combines machine learning models with a FastAPI backend and a React frontend to deliver real-time predictions, visual analytics, and explainable insights.

Key Features
 Loan Default Prediction using ML models
 Risk Classification (Low / Medium / High)
 Action Recommendations (Approve / Review / Reject)
 Explainable AI (Reasons for prediction)
 Interactive Charts (Gauge + Bar using Plotly)
 Prediction History (stored in localStorage)
 Banking-Style Dashboard UI
 FastAPI Backend for real-time processing

System Architecture
User → React UI → Axios → FastAPI → ML Model → JSON → UI

Tech Stack
🔹 Frontend
React.js
Axios
Plotly.js
CSS
🔹 Backend
FastAPI
Uvicorn
Python
🔹 Machine Learning
Scikit-learn
XGBoost / LightGBM
🔹 Data Processing
Pandas
NumPy

Project Structure
creditpathai/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Form.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Charts.js
│   │   │   ├── History.js
│   │   ├── App.js
│
├── main.py
├── model.pkl
├── pipeline.pkl
└── README.md

Installation & Setup
🔹 1. Clone Repository
git clone https://github.com/your-username/creditpathai.git
cd creditpathai
🔹 2. Backend Setup
pip install -r requirements.txt
uvicorn main:app --reload

Backend will run at:
http://127.0.0.1:8000

 API Docs:
http://127.0.0.1:8000/docs
🔹 3. Frontend Setup
cd frontend
npm install
npm start

Frontend will run at:
http://localhost:3000

 API Endpoint
POST /predict
🔹 Input
{
  "age": 35,
  "loanamount": 10000,
  "creditscore": 720,
  "monthsemployed": 24,
  "numcreditlines": 3,
  "interestrate": 5.5,
  "loanterm": 36,
  "dtiratio": 0.2
}
🔹 Output
{
  "probability": 0.32,
  "risk": "Medium",
  "action": "Review Manually ",
  "reasons": [
    "High Loan Amount"
  ]


Risk Classification Logic
Probability	Risk Level	Action
< 0.25	Low	Approve Loan
0.25 – 0.50	Medium	Review Manually
> 0.50	High	Reject Loan

Data Visualization
 Gauge Chart → Displays risk probability
 Bar Chart → Shows risk category distribution

Explainable AI
The system provides reasons for predictions such as:
 Low Credit Score
 High Debt-to-Income Ratio
 Low Employment Stability
 High Loan Amount
 High Interest Rate

This improves transparency and helps users understand model decisions.
 Additional Features
 Prediction history (stored in localStorage)
 Filter by risk level
 Professional banking-style UI
 Real-time API integration

Testing
Tested with low, medium, and high-risk inputs
Verified:
API response correctness
UI updates
Chart accuracy

 Challenges Faced
CORS issues between frontend and backend
API integration bugs
Risk threshold tuning
UI design improvements


 Future Enhancements
Cloud deployment (Render / Vercel)
Database integration (MongoDB)
Authentication system
Real-time financial data integration
Advanced Explainable AI (SHAP / LIME)


