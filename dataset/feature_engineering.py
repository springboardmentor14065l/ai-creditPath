# ============================================================
# CreditPathAI – Feature Engineering
# Student : Akhil Babu Gujjaralapudi
# Follows : Feature Engineering Handout (mentor guide)
# Input   : Loan_default.csv
# Output  : final_features.csv
# ============================================================

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# STEP 1: LOAD CLEAN DATASET
# ============================================================
print("=" * 60)
print("STEP 1: Load Clean Dataset")
print("=" * 60)

df = pd.read_csv('Loan_default.csv')

# Rename columns to standard names
df.rename(columns={
    'Age'            : 'age',
    'Income'         : 'income',
    'LoanAmount'     : 'loan_amount',
    'CreditScore'    : 'credit_score',
    'MonthsEmployed' : 'months_employed',
    'NumCreditLines' : 'num_credit_lines',
    'InterestRate'   : 'interest_rate',
    'LoanTerm'       : 'loan_term',
    'DTIRatio'       : 'dti_ratio',
    'Education'      : 'education',
    'EmploymentType' : 'employment_type',
    'MaritalStatus'  : 'marital_status',
    'HasMortgage'    : 'has_mortgage',
    'HasDependents'  : 'has_dependents',
    'LoanPurpose'    : 'loan_purpose',
    'HasCoSigner'    : 'has_cosigner',
    'Default'        : 'default_status'
}, inplace=True)

# Drop LoanID (not useful for prediction)
if 'LoanID' in df.columns:
    df.drop(columns=['LoanID'], inplace=True)

print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# ============================================================
# STEP 2: LOAN TO INCOME RATIO
# ============================================================
print("\nSTEP 2: Loan to Income Ratio")
df['loan_income_ratio'] = df['loan_amount'] / df['income']
print("✅ loan_income_ratio created — High loan vs income = higher risk")

# ============================================================
# STEP 3: CREDIT UTILIZATION PROXY
# ============================================================
print("\nSTEP 3: Credit Utilization Proxy")
df['credit_utilization'] = df['loan_amount'] / df['num_credit_lines'].replace(0, 1)
print("✅ credit_utilization created — More debt per credit line = higher risk")

# ============================================================
# STEP 4: INTEREST BURDEN
# ============================================================
print("\nSTEP 4: Interest Burden")
df['interest_burden'] = df['loan_amount'] * df['interest_rate']
print("✅ interest_burden created — Higher interest = repayment difficulty")

# ============================================================
# STEP 5: EMPLOYMENT STABILITY
# ============================================================
print("\nSTEP 5: Employment Stability")
df['employment_stability'] = df['months_employed'] / df['age'].replace(0, 1)
print("✅ employment_stability created — Stable employment = lower risk")

# ============================================================
# STEP 6: DEBT TO INCOME FLAG
# ============================================================
print("\nSTEP 6: High DTI Flag")
df['high_dti_flag'] = (df['dti_ratio'] > 0.5).astype(int)
print("✅ high_dti_flag created — DTI > 0.5 = strong default indicator")

# ============================================================
# STEP 7: CREDIT SCORE BUCKETING
# ============================================================
print("\nSTEP 7: Credit Score Bucketing")
df['credit_score_bucket'] = pd.cut(
    df['credit_score'],
    bins=[0, 600, 700, 800, 900],
    labels=['Poor', 'Average', 'Good', 'Excellent']
)
df = pd.get_dummies(df, columns=['credit_score_bucket'], drop_first=False)
print("✅ credit_score_bucket created and one-hot encoded")

# ============================================================
# STEP 8: LOG TRANSFORM INCOME
# ============================================================
print("\nSTEP 8: Log Transform Income")
df['log_income'] = np.log1p(df['income'])
print("✅ log_income created — Stabilizes skewed income distribution")

# ============================================================
# STEP 9: INTERACTION FEATURE
# ============================================================
print("\nSTEP 9: Income-Loan Interaction")
df['income_loan_interaction'] = df['income'] * df['loan_amount']
print("✅ income_loan_interaction created — Captures combined financial pressure")

# ============================================================
# STEP 10: ENCODE REMAINING CATEGORICAL COLUMNS
# ============================================================
print("\nSTEP 10: Encode Categorical Columns")

cat_cols = ['education', 'employment_type', 'marital_status', 'loan_purpose']
df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

# Encode binary columns (Yes/No → 1/0)
binary_cols = ['has_mortgage', 'has_dependents', 'has_cosigner']
for col in binary_cols:
    df[col] = df[col].map({'Yes': 1, 'No': 0}).fillna(df[col])
    print(f"✅ {col} encoded")

print("✅ All categorical columns encoded")

# ============================================================
# STEP 11: DROP WEAK/REDUNDANT FEATURES
# ============================================================
print("\nSTEP 11: Drop Weak/Redundant Features")

# Drop raw income since log_income replaces it
drop_cols = ['income']
df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)
print("✅ Dropped raw income (replaced by log_income)")

# ============================================================
# STEP 12: FINAL DATASET SAVE
# ============================================================
print("\nSTEP 12: Save Final Feature Dataset")

df.to_csv('final_features.csv', index=False)

print(f"\n✅ final_features.csv saved!")
print(f"   Rows    : {df.shape[0]}")
print(f"   Columns : {df.shape[1]}")
print(f"   Features: {[c for c in df.columns if c != 'default_status']}")

print("\n" + "=" * 60)
print("✅ FEATURE ENGINEERING COMPLETE!")
print("=" * 60)
print("\nOutput: final_features.csv")
print("Next  : Milestone 3 — Logistic Regression Baseline Model")
