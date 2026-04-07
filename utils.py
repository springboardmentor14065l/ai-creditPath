import pandas as pd
import numpy as np

def feature_engineering(data):
    df = data.copy()
    
    # From final_features.py
    df['loan_income_ratio'] = df['loan_amount'] / (df['income'] + 1e-6)
    df['credit_utilization'] = df['loan_amount'] / (df['num_credit_lines'] + 1e-6)
    df['interest_burden'] = df['loan_amount'] * df['interest_rate']
    df['employment_stability'] = df['months_employed'] / (df['age'] + 1e-6)
    df['high_dti_flag'] = (df['dti_ratio'] > 0.5).astype(int)
    
    # Credit Score Bucketing
    df['credit_score_bucket_Poor'] = (df['credit_score'] <= 600).astype(int)
    df['credit_score_bucket_Average'] = ((df['credit_score'] > 600) & (df['credit_score'] <= 700)).astype(int)
    df['credit_score_bucket_Good'] = ((df['credit_score'] > 700) & (df['credit_score'] <= 800)).astype(int)
    df['credit_score_bucket_Excellent'] = (df['credit_score'] > 800).astype(int)
    
    df['log_income'] = np.log1p(df['income'])
    df['income_loan_interaction'] = df['income'] * df['loan_amount']
    
    # From advanced_model_training.py
    df['interest_rate_score_interaction'] = df['interest_rate'] * (1000 - df['credit_score'])
    df['monthly_interest_burden'] = df['interest_burden'] / df['loan_term']
    
    # Drop original income as it was transformed
    if 'income' in df.columns:
        df = df.drop(columns=['income'])
        
    # Reorder columns to match model training
    expected_cols = [
        'age', 'loan_amount', 'credit_score', 'months_employed', 'num_credit_lines',
        'interest_rate', 'loan_term', 'dti_ratio', 'education', 'employment_type',
        'marital_status', 'has_mortgage', 'has_dependents', 'loan_purpose', 'has_cosigner',
        'loan_income_ratio', 'credit_utilization', 'interest_burden', 'employment_stability',
        'high_dti_flag', 'credit_score_bucket_Poor', 'credit_score_bucket_Average',
        'credit_score_bucket_Good', 'credit_score_bucket_Excellent', 'log_income',
        'income_loan_interaction', 'interest_rate_score_interaction', 'monthly_interest_burden'
    ]
    
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0
            
    return df[expected_cols]
