import pandas as pd
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine("postgresql://postgres:malleswari%40123@localhost:5432/creditpath")

# Load dataset from database
df = pd.read_sql("SELECT * FROM loan_default", engine)

print("Dataset Loaded Successfully\n")

# ----------------------------
# 1. Remove duplicate rows
# ----------------------------
df = df.drop_duplicates()

# ----------------------------
# 2. Handle missing values
# ----------------------------
df = df.dropna()

# ----------------------------
# 3. Convert categorical columns
# ----------------------------

df['education'] = df['education'].astype('category').cat.codes
df['employment_type'] = df['employment_type'].astype('category').cat.codes
df['marital_status'] = df['marital_status'].astype('category').cat.codes
df['loan_purpose'] = df['loan_purpose'].astype('category').cat.codes

# Convert Yes/No columns to 1/0

df['has_mortgage'] = df['has_mortgage'].map({'Yes':1,'No':0})
df['has_dependents'] = df['has_dependents'].map({'Yes':1,'No':0})
df['has_cosigner'] = df['has_cosigner'].map({'Yes':1,'No':0})

# ----------------------------
# 4. Remove ID column
# ----------------------------
df = df.drop(columns=['loan_id'])

# ----------------------------
# 5. Save cleaned dataset
# ----------------------------
df.to_csv("clean_loans.csv", index=False)

print("Clean dataset saved as clean_loans.csv")
print("Final dataset shape:", df.shape)