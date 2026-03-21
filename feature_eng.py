import pandas as pd
import numpy as np

# STEP 1: Load cleaned dataset
df = pd.read_csv("data/clean_loans.csv")

print("Original shape:", df.shape)

# STEP 2: Create new features

# 1. Loan to Income Ratio
df['loan_income_ratio'] = df['loan_amnt'] / df['annual_inc']

# 2. Interest Burden
df['interest_burden'] = df['loan_amnt'] * df['int_rate']

# 3. High DTI Flag (adjusted threshold)
df['high_dti_flag'] = (df['dti'] > 20).astype(int)

# 4. Log Income (handle skewness)
df['log_income'] = np.log1p(df['annual_inc'])

# 5. Interaction Feature
df['income_loan_interaction'] = df['annual_inc'] * df['loan_amnt']

# STEP 3: Optional cleanup (remove redundant column)
df = df.drop(columns=['annual_inc'])

print("New shape after feature engineering:", df.shape)

# STEP 4: Save final dataset
df.to_csv("data/final_features.csv", index=False)

print("✅ Feature engineering completed successfully!")