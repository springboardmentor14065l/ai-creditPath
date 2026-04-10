import pandas as pd
import numpy as np


# STEP 1: Load cleaned dataset
df = pd.read_csv("data/clean_loans.csv")

print("Original shape:", df.shape)


df['loan_income_ratio'] = df['loan_amnt'] / df['annual_inc']

df['interest_burden'] = df['loan_amnt'] * df['int_rate']

df['high_dti_flag'] = (df['dti'] > 20).astype(int)

df['log_income'] = np.log1p(df['annual_inc'])

df['income_loan_interaction'] = df['annual_inc'] * df['loan_amnt']


# 1. Credit risk interaction
df["credit_risk_score"] = df["int_rate"] * df["dti"]

# 2. Repayment pressure
df["repayment_pressure"] = df["installment"] / (df["loan_amnt"] + 1)

# 3. Risk grade score (important)
df["risk_grade_score"] = (
    df.get("grade_B", 0)*1 +
    df.get("grade_C", 0)*2 +
    df.get("grade_D", 0)*3 +
    df.get("grade_E", 0)*4 +
    df.get("grade_F", 0)*5 +
    df.get("grade_G", 0)*6
)

# 4. Non-linear transformation
df["dti_log"] = np.log1p(df["dti"])

# 5. Loan burden (refined)
df["loan_burden"] = df["loan_amnt"] * df["int_rate"]

# 6. EMI to income ratio (very useful)
df["emi_to_income"] = df["installment"] / (df["annual_inc"] + 1)



df = df.drop(columns=['annual_inc'])



print("New shape after feature engineering:", df.shape)
print("Columns now:", df.columns)



df.to_csv("data/final_features.csv", index=False)

print("✅ Feature engineering completed successfully!")