# CreditPathAI — Milestone 6: Frontend Dashboard

**Student:** Akhil Babu Gujjaralapudi  
**Internship:** Infosys Springboard 6.0  
**Mentor:** M. Likhita  

---

## Project Overview

CreditPathAI is a full-stack ML platform that predicts loan default risk and recommends recovery actions.
This milestone delivers the React.js frontend dashboard that integrates with the FastAPI backend.

---

## Setup Guide

### Step 1 — Start the FastAPI backend first
```bash
cd dataset
python -m uvicorn main:app --reload
```
API will run at: http://127.0.0.1:8000

### Step 2 — Install frontend dependencies
```bash
cd frontend
npm install
```

### Step 3 — Start the React app
```bash
npm start
```
Frontend will open at: http://localhost:3000

---

## Folder Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.js    ← Result display with risk level + action
│   │   ├── Form.js         ← Borrower input form
│   │   └── Charts.js       ← Plotly analytics charts
│   ├── services/
│   │   └── api.js          ← Axios API calls to FastAPI
│   ├── App.js              ← Main app with tabs and routing
│   └── App.css             ← Full styling
└── README.md
```

---

## API Endpoints Used

| Method | Endpoint        | Purpose                        |
|--------|-----------------|--------------------------------|
| GET    | /health         | API status check               |
| GET    | /risk-info      | Risk threshold information     |
| POST   | /predict        | Single borrower prediction     |
| POST   | /predict-batch  | Multiple borrower predictions  |

---

## Features

- **Predict Tab** — Input borrower details, get risk level + recommended action instantly
- **Analytics Tab** — Bar chart, pie chart, and probability trend (updates with each prediction)
- **History Tab** — Full table of all predictions made in the session
- **API Status Indicator** — Shows if FastAPI is running (green = online, red = offline)
- **Color-coded Results** — Green (Low), Orange (Medium), Red (High)
- **Probability Bar** — Visual representation of default probability
- **Responsive Design** — Works on desktop and mobile

---

## Risk Thresholds

| Risk Level | Probability Range | Action                        |
|------------|-------------------|-------------------------------|
| Low        | < 30%             | Send Reminder                 |
| Medium     | 30% – 60%         | Call Customer                 |
| High       | ≥ 60%             | Immediate Recovery Action     |

---

## Test Cases for UAT

**High Risk:**
- Age: 35, Income: 30000, Loan: 120000, Credit Score: 520, DTI: 0.85, Employment: Unemployed

**Medium Risk:**
- Age: 42, Income: 65000, Loan: 80000, Credit Score: 620, DTI: 0.52, Employment: Part-time

**Low Risk:**
- Age: 50, Income: 130000, Loan: 40000, Credit Score: 800, DTI: 0.20, Employment: Full-time

---

## Tech Stack

| Layer    | Technology              |
|----------|-------------------------|
| Frontend | React.js                |
| Charts   | Plotly.js               |
| HTTP     | Axios                   |
| Backend  | FastAPI (Python)        |
| Model    | XGBoost                 |
| Styling  | Custom CSS + DM Sans    |
