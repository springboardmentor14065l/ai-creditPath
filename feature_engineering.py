import pandas as pd
import numpy as np

# -----------------------------
# Step 1 – Load Clean Dataset
# -----------------------------
df = pd.read_csv("clean_loans.csv")

# -----------------------------
# Step 2 – Loan to Income Ratio
# -----------------------------
df['loan_income_ratio'] = df['loanamount'] / (df['income'] + 1)

# -----------------------------
# Step 3 – Credit Utilization Proxy
# -----------------------------
df['credit_utilization'] = df['loanamount'] / (df['numcreditlines'] + 1)

# -----------------------------
# Step 4 – Interest Burden
# -----------------------------
df['interest_burden'] = df['loanamount'] * df['interestrate']

# -----------------------------
# Step 5 – Employment Stability
# -----------------------------
df['employment_stability'] = df['monthsemployed'] / (df['age'] + 1)

# -----------------------------
# Step 6 – Debt to Income Flag
# -----------------------------
df['high_dti_flag'] = (df['dtiratio'] > 0.5).astype(int)

# -----------------------------
# Step 7 – Credit Score Bucketing
# -----------------------------
# NOTE: Your data is scaled, so adjusted bins
df['credit_score_bucket'] = pd.cut(
    df['creditscore'],
    bins=[-2, -0.5, 0, 0.5, 2],
    labels=['Poor', 'Average', 'Good', 'Excellent']
)

df = pd.get_dummies(df, columns=['credit_score_bucket'], drop_first=True)

# -----------------------------
# Step 8 – Log Transform Income
# -----------------------------
df['log_income'] = np.log1p(df['income'])

# -----------------------------
# Step 9 – Interaction Feature
# -----------------------------
df['income_loan_interaction'] = df['income'] * df['loanamount']

# -----------------------------
# Step 10 – Drop Weak Features
# -----------------------------
df = df.drop(columns=['income'])  # as suggested

# -----------------------------
# Step 11 – Handle Missing Values
# -----------------------------
df.fillna(df.median(numeric_only=True), inplace=True)

# -----------------------------
# Step 12 – Save Final Dataset
# -----------------------------
df.to_csv("final_features.csv", index=False)

print("✅ Feature Engineering Completed Successfully!")