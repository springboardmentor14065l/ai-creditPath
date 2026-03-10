import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler

# Step 1 – Connect Python to PostgreSQL
engine = create_engine("postgresql://postgres:8108289082@localhost:5432/CreditPathAI")

df = pd.read_sql("SELECT * FROM public.loan_default", engine)

print("Dataset Loaded Successfully")

#  Inspect Dataset Structure
print("\nDataset Structure")
print(df.info())

#  Identify Missing Values
print("\nMissing Values")
print(df.isnull().sum())

#  missing values
df['income'].fillna(df['income'].median(), inplace=True)
df['loanamount'].fillna(df['loanamount'].median(), inplace=True)

#  Detect Duplicate Records
print("\nDuplicate Records:", df.duplicated().sum())

df = df.drop_duplicates()

#  Verify Column Datatypes
print("\nColumn Data Types")
print(df.dtypes)

#  Remove Non-Predictive Columns
df = df.drop(columns=['loanid'])

#  Detect Outliers (basic statistics)
print("\nStatistical Summary")
print(df.describe())

#  Encode Categorical Variables
df = pd.get_dummies(df, drop_first=True)

# Converting column names to lowercase
df.columns = df.columns.str.lower()

#  Scale Numerical Features
scaler = StandardScaler()

df[['income','loanamount','creditscore']] = scaler.fit_transform(
    df[['income','loanamount','creditscore']]
)

#  Save Clean Dataset
df.to_csv("clean_loans.csv", index=False)

print("\nData Cleaning Completed Successfully")
print("Clean dataset saved as clean_loans.csv")