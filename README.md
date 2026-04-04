# ai-creditPath
# AI Credit Path – Loan Default Prediction System

## Project Title
AI Credit Path: Loan Approval and Default Risk Prediction

## Problem Statement
Financial institutions face challenges in identifying whether a loan applicant will repay the loan or default. Incorrect decisions may lead to financial losses. There is a need for a data-driven system that can analyze applicant information and predict loan repayment behavior.

## Objective
The objective of this project is to develop a machine learning model that predicts loan approval and default risk using historical lending data (Lending Club dataset). The system will assist financial institutions in making informed and accurate lending decisions.

## Key Performance Indicators (KPIs)

The success of the project will be measured using:

- Model Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- Default Prediction Rate
- Loan Approval Prediction Accuracy

## Expected Outcome
A trained predictive model that can analyze applicant financial details and determine the probability of loan repayment or default. This system will help reduce financial risk and improve decision-making efficiency.


## Dataset

Source: Kaggle Loan Dataset

Original Dataset:
- Rows: 2,260,668
- Columns: 145

Cleaned Dataset:
- Rows: 2,258,953
- Columns: 8

Selected Features:
- loan_amnt
- term
- int_rate
- installment
- grade
- annual_inc
- dti
- loan_status


## Milestone 4: Advanced Model Analysis

### What I did

In this milestone, I tried to improve my model using advanced algorithms like XGBoost and LightGBM.

I also:
- Created additional features from the existing data  
- Tried tuning model parameters  
- Tested different approaches to improve accuracy  

### Results

| Model                | AUC Score |
|---------------------|----------|
| Logistic Regression | 0.72     |
| XGBoost             | 0.7019   |
| LightGBM            | 0.7016   |


### What I observed

Even after trying different methods, the advanced models did not perform better than Logistic Regression.

The scores stayed almost the same or slightly lower.


### Conclusion

This shows that the dataset mostly follows simple patterns, and Logistic Regression is already able to capture it well.

So, using more complex models did not give better results in this case.

### Final Note

Even though the score did not increase, this step helped me understand how different models behave and how important the data is compared to the model.