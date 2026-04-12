# CreditPathAI

## 📌 Project Overview

CreditPathAI is an AI-powered system designed to automate and optimize the loan recovery lifecycle.  
It uses machine learning techniques to analyze borrower data and predict loan default risk, helping financial institutions make faster and smarter decisions.

This project is developed as part of an academic/individual major project.

---

## 🎯 Objective

The main goal of CreditPathAI is to:
- Predict loan default risk using machine learning models
- Improve loan recovery efficiency
- Assist financial decision-making using data-driven insights
- Reduce manual effort in credit risk analysis

---

## 🧠 Key Features

- Data preprocessing and feature engineering
- Machine learning models for risk prediction (Logistic Regression / XGBoost / LightGBM)
- Risk scoring system for borrowers
- Recommendation engine for loan actions
- API prototype for model deployment (FastAPI)
- Performance evaluation using AUC-ROC and accuracy

---

## 📊 Dataset Features

- Age
- Loan Amount
- Credit Score
- Months Employed
- Number of Credit Lines
- Interest Rate
- Loan Term
- Debt-to-Income Ratio
- Employment Type
- Education Level
- Marital Status
- Mortgage / Dependents status

---

## 🏗️ Project Structure
CreditPathAI/
│
├── data/ # Dataset files
├── notebooks/ # Jupyter notebooks (EDA, training)
├── models/ # Saved ML models
├── backend/ # API (FastAPI / Flask)
├── frontend/ # UI (if applicable)
├── src/ # Core Python scripts
│ ├── preprocessing.py
│ ├── training.py
│ ├── prediction.py
│
├── requirements.txt
├── README.md
└── .gitignore


---

## ⚙️ Technologies Used

- Python
- Pandas / NumPy
- Scikit-learn
- XGBoost / LightGBM
- FastAPI (for API prototype)
- Matplotlib / Seaborn
- Git & GitHub

---

## 🚀 How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/your-username/CreditPathAI.git
2. Move into project directory
cd CreditPathAI
3. Install dependencies
pip install -r requirements.txt
4. Run main script / notebook
python src/training.py
OR start API (if available)
uvicorn backend.main:app --reload

## Model Performance
Logistic Regression: Baseline model
XGBoost: High accuracy with non-linear patterns
LightGBM: Optimized performance and speed
Evaluation Metric: AUC-ROC Score

## Future Improvements
Deploy model on cloud (AWS / Render )
Add real-time loan scoring dashboard
Improve explainability using SHAP
Add fraud detection module
Build full-stack web application
