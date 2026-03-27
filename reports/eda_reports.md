# 📊 EDA Report – CreditPathAI

## 1. Dataset Overview

* **Dataset Name:** Loan Default Dataset
* **Total Records:** 255,347
* **Total Features:** 18

---

## 2. Data Structure

* **Numerical Features:** 10
* **Categorical Features:** 8

### Key Columns:

* Age
* Income
* LoanAmount
* CreditScore
* InterestRate
* DTIRatio
* **Target Variable:** Default

---

## 3. Data Quality Check

### Missing Values

* ✅ No missing values found in dataset
* Dataset is clean and ready for modeling

### Data Types

* Numerical: int64, float64
* Categorical: object

---

## 4. Key Visualizations & Insights

### 4.1 Default Distribution

* Non-Defaulters: **88.39%**
* Defaulters: **11.61%**

👉 Dataset is **imbalanced** (important for ML model)

---

### 4.2 Loan Amount Distribution

* Loan amounts range from **15,000 to 150,000**
* Most loans are concentrated around:

  * **~82,000 (median)**

👉 Higher loan amounts tend to increase financial risk

---

### 4.3 Income Analysis

* Average income: **~82,499**
* Range: **15,000 – 149,999**

👉 Wide income distribution → strong feature for prediction

---

### 4.4 Credit Score Insights

* Credit score is a **critical risk indicator**
* Lower credit score → higher probability of default

---

### 4.5 Debt-to-Income Ratio (DTI)

* Average DTI: **0.50**
* Range: **0.1 – 0.9**

👉 Higher DTI → higher financial burden → more default risk

---

### 4.6 Employment & Stability

* Features like:

  * MonthsEmployed
  * EmploymentType

👉 Stable employment reduces default probability

---

### 4.7 Correlation Analysis

Key relationships observed:

* 📈 LoanAmount ↑ → Default ↑
* 📉 CreditScore ↓ → Default ↑
* 📈 DTIRatio ↑ → Default ↑

👉 Strong predictors for ML model:

* CreditScore
* DTIRatio
* LoanAmount
* Income

---

## 5. Key Findings

1. Dataset is **clean (no missing values)**
2. Default rate is **~11.6% (imbalanced dataset)**
3. Credit score is the **strongest predictor**
4. High DTI ratio significantly increases risk
5. Loan amount and income influence repayment behavior
6. Employment stability plays an important role

---

## 6. Conclusion

The dataset shows clear patterns in borrower behavior:

* Financial indicators strongly impact default risk
* Data is suitable for **machine learning modeling**
* No major preprocessing issues → ready for next stage

---

## 7. Next Steps

* Feature Engineering
* Handle class imbalance
* Train models:

  * Logistic Regression
  * XGBoost / LightGBM
* Model Evaluation

---
