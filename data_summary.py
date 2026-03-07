import pandas as pd

df = pd.read_csv("data/cleaned_loan_data.csv")

print("First 5 rows:")
print(df.head())

print("\nDataset Information:")
print(df.info())

print("\nLoan Status Count:")
print(df["loan_status"].value_counts())