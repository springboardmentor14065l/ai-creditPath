import pandas as pd

# Load dataset
df = pd.read_csv("data/loan.csv", low_memory=False)

print("Original shape:", df.shape)

# Columns we will keep
columns = [
    "loan_amnt",
    "term",
    "int_rate",
    "installment",
    "grade",
    "annual_inc",
    "dti",
    "loan_status"
]

# Keep only these columns
df = df[columns]

# Remove missing values
df = df.dropna()

print("Cleaned shape:", df.shape)

# Save cleaned dataset
df.to_csv("data/cleaned_loan_data.csv", index=False)

print("✅ Data cleaning completed!")