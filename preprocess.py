import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv("Loan_default.csv")

# Remove missing values
df = df.dropna()

# Identify non-numeric columns
non_numeric_columns = df.select_dtypes(include=['object']).columns

# Encode non-numeric columns using LabelEncoder
label_encoders = {}
for column in non_numeric_columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Overwrite the original dataset with preprocessed data
df.to_csv("Loan_default.csv", index=False)

# Debugging: Print the first few rows and column data types
print("First few rows of the preprocessed dataset:")
print(df.head())
print("\nColumn data types:")
print(df.dtypes)

print("Preprocessing complete. Non-numeric columns encoded and saved to Loan_default.csv.")