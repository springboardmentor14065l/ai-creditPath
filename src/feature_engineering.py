import pandas as pd
import numpy as np

df = pd.read_csv("../data/clean_loans.csv")

# ----------------------------
# BASIC FEATURES
# ----------------------------
df['loan_income_ratio'] = df['loan_amount'] / (df['income'] + 1)

df['interest_burden'] = df['loan_amount'] * df['rate_of_interest']

df['ltv_risk'] = df['LTV'] / 100

df['high_dti_flag'] = (df['dtir1'] > 40).astype(int)

# ----------------------------
# 🔥 UNIQUE FEATURES (YOUR EDGE)
# ----------------------------

# 1. Financial Stress Index
df['financial_stress_index'] = (
    df['loan_amount'] * df['rate_of_interest']
) / (df['income'] + 1)

# 2. Risk Interaction
df['risk_interaction'] = df['dtir1'] * df['LTV']

# 3. Income Stability
df['income_stability'] = df['income'] / (df['loan_amount'] + 1)

# ----------------------------
# TRANSFORMATIONS
# ----------------------------

df['log_income'] = np.log1p(df['income'])

df['income_loan_interaction'] = df['income'] * df['loan_amount']

# ----------------------------
# CLEANUP
# ----------------------------

df = df.drop(columns=['income'])

df.to_csv("../data/final_features.csv", index=False)

print("✅ Feature engineering completed")