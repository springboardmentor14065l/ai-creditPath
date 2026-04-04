import pandas as pd

# STEP 1: Load dataset
df = pd.read_csv("data/loan.csv", low_memory=False)

print("Original shape:", df.shape)

# STEP 2: Reduce dataset size
df = df.sample(n=200000, random_state=42)

# STEP 3: Select useful columns
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

df = df[columns]

# STEP 4: Handle missing values
df['annual_inc'] = df['annual_inc'].fillna(df['annual_inc'].median())
df['dti'] = df['dti'].fillna(df['dti'].median())

df = df.dropna()

# STEP 5: Convert target variable
df = df[df['loan_status'].isin(['Fully Paid', 'Charged Off'])]

df['default_status'] = df['loan_status'].apply(
    lambda x: 1 if x == 'Charged Off' else 0
)

df = df.drop('loan_status', axis=1)


df['term'] = df['term'].astype(str).str.extract(r'(\d+)').astype(int)

df['int_rate'] = df['int_rate'].astype(str).str.replace('%', '', regex=False).astype(float)

df = pd.get_dummies(df, columns=['grade'], drop_first=True)

# STEP 7: Remove duplicates
df = df.drop_duplicates()

print("Cleaned shape:", df.shape)

# STEP 8: Save dataset
df.to_csv("data/clean_loans.csv", index=False)

print("✅ Data cleaning completed successfully!")