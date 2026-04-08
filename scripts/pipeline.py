import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler

# --- PATH CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')
MODELS_DIR = os.path.join(SCRIPT_DIR, '..', 'models')

# --- DATABASE CREDENTIALS (READ-ONLY MODE) ---
# This script will ONLY read data and will NOT perform any write operations.
USER = "postgres"
PASS = "nex"
HOST = "localhost"
PORT = "5432"
DB_NAME = "creditpath"

# --- STEP 1: Extract Data from PostgreSQL ---
print(f"Connecting to PostgreSQL Database: {DB_NAME} (READ-ONLY)...")
connection_url = f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}"
engine = create_engine(connection_url)

try:
    # Attempt to read from the database
    df = pd.read_sql("SELECT * FROM loan_default", engine)
    print("Step 1 Complete: Data successfully extracted from PostgreSQL.")
except Exception as e:
    print(f"\n[Database Read Error]: {e}")
    print("Falling back to local data/Loan_default.csv...")
    df = pd.read_csv(os.path.join(DATA_DIR, 'Loan_default.csv'))

# Normalize column names
df.columns = [col.lower() for col in df.columns]
df = df.rename(columns={
    'loanid': 'loan_id', 
    'default': 'default_status',
    'loanamount': 'loan_amount',
    'creditscore': 'credit_score',
    'numcreditlines': 'num_credit_lines',
    'interestrate': 'interest_rate',
    'monthsemployed': 'months_employed',
    'loanterm': 'loan_term',
    'dtiratio': 'dti_ratio'
})

# --- STEP 2: Inspect Dataset Structure ---
print("\nStep 2: Dataset Structure:")
df.info()

# --- STEP 3: Identify Missing Values ---
print("\nStep 3: Checking for Missing Values...")
for col in df.select_dtypes(include=[np.number]).columns:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].median())
        print(f"Missing values in '{col}' handled using median.")

# --- STEP 4: Detect Duplicate Records ---
dup_count = df.duplicated().sum()
if dup_count > 0:
    df = df.drop_duplicates()
    print(f"Step 4: {dup_count} duplicates removed.")
else:
    print("Step 4: No duplicates found.")

# --- STEP 5: Verify Column Datatypes ---
print("\nStep 5: Verifying Column Datatypes...")

# --- STEP 6: Remove Non-Predictive Columns ---
if 'loan_id' in df.columns:
    df = df.drop(columns=['loan_id'])
    print("Step 6: Removed 'loan_id'.")

# --- ADVANCED FEATURE ENGINEERING (New Step) ---
print("\nStep 7: Performing Advanced Feature Engineering...")

# 2. Loan to Income Ratio
df['loan_to_income'] = df['loan_amount'] / df['income']

# 3. Credit Utilization Proxy
df['credit_utilization'] = df['loan_amount'] / df['num_credit_lines']

# 4. Interest Burden
df['interest_burden'] = df['loan_amount'] * df['interest_rate']

# 5. Employment Stability
df['employment_stability'] = df['months_employed'] / df['age']

# 6. Debt to Income Flag (High DTI > 0.5)
df['high_dti_flag'] = (df['dti_ratio'] > 0.5).astype(int)

# 7. Credit Score Bucketing
bins = [0, 600, 700, 800, 900]
labels = ['Poor', 'Average', 'Good', 'Excellent']
df['credit_score_bucket'] = pd.cut(df['credit_score'], bins=bins, labels=labels)

# 8. Log Transform Income (for stability)
df['log_income'] = np.log1p(df['income'])

# 9. Interaction Feature
df['income_loan_interaction'] = df['income'] * df['loan_amount']

print("Advanced Feature Engineering Complete.")

# --- STEP 8: Detect Outliers ---
print("\nStep 8: Handling Outliers in Income...")
upper_limit = df['income'].quantile(0.99)
df.loc[df['income'] > upper_limit, 'income'] = upper_limit

# --- STEP 9: Encode Categorical Variables ---
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
print(f"Step 9: Encoding categorical variables: {cat_cols}")
df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

import joblib

# --- STEP 10: Scale Numerical Features ---
scaler = StandardScaler()
# Scale both original and engineered numerical features
cols_to_scale = ['income', 'loan_amount', 'credit_score', 'loan_to_income', 'credit_utilization', 'interest_burden', 'employment_stability', 'log_income', 'income_loan_interaction']
available_cols = [c for c in cols_to_scale if c in df.columns]
df[available_cols] = scaler.fit_transform(df[available_cols])
print(f"Step 10: Scaled numerical features: {available_cols}")

# Save the scaler for use in prediction
scaler_path = os.path.join(MODELS_DIR, 'scaler.joblib')
joblib.dump(scaler, scaler_path)
print(f"StandardScaler saved as '{scaler_path}'.")

# --- STEP 11: Save the Clean Dataset Locally ---
# NOTE: We save the result locally to CSV and DO NOT write back to the DB.
output_path = os.path.join(DATA_DIR, "clean_loans.csv")
df.to_csv(output_path, index=False)
print(f"\nStep 11: Clean dataset saved as '{output_path}'.")
print("\nFull Data Pipeline Execution Complete (Read-Only Mode - No DB Changes).")
