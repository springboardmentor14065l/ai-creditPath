# STEP 1: Import Libraries
import pandas as pd
import numpy as np

# STEP 2: Load Dataset
df = pd.read_csv("clean_loans.csv")

print("Initial Data:")
print(df.head())

# -------------------------------
# FEATURE ENGINEERING STARTS
# -------------------------------

# 1. Loan to Income Ratio
df['loan_income_ratio'] = df['loan_amount'] / df['income']

# 2. Credit Utilization
df['credit_utilization'] = df['loan_amount'] / df['num_credit_lines']

# 3. Interest Burden
df['interest_burden'] = df['loan_amount'] * df['interest_rate']

# 4. Employment Stability
df['employment_stability'] = df['months_employed'] / df['age']

# 5. High DTI Flag
df['high_dti_flag'] = (df['dti_ratio'] > 0.5).astype(int)

# 6. Credit Score Bucketing
df['credit_score_bucket'] = pd.cut(
    df['credit_score'],
    bins=[0, 600, 700, 800, 900],
    labels=['Poor', 'Average', 'Good', 'Excellent']
)

# Convert categorical to numeric (One-Hot Encoding)
df = pd.get_dummies(df, columns=['credit_score_bucket'])

# 7. Log Transform Income
df['log_income'] = np.log1p(df['income'])

# 8. Interaction Feature
df['income_loan_interaction'] = df['income'] * df['loan_amount']

# 9. Drop Redundant Columns
df = df.drop(columns=['income'])

# -------------------------------
# FINAL CHECK
# -------------------------------
print("\nFinal Data Columns:")
print(df.columns)

print("\nFinal Data Sample:")
print(df.head())

# -------------------------------
# SAVE FILE
# -------------------------------
df.to_csv("final_features.csv", index=False)

print("\n✅ final_features.csv created successfully!")