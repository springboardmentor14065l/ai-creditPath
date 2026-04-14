import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:Sham%408029@localhost:5432/creditpath"
)

df = pd.read_sql("SELECT * FROM loan_default", engine)

print(df.head())
df.info()
print(df.isnull().sum())

df = df.drop(columns=["ID"])

num_cols = [
"rate_of_interest",
"Interest_rate_spread",
"Upfront_charges",
"property_value",
"income",
"LTV",
"dtir1",
"term"
]

for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

cat_cols = [
"loan_limit",
"approv_in_adv",
"loan_purpose",
"Neg_ammortization",
"age",
"submission_of_application"
]

for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

print(df.isnull().sum())

df = pd.get_dummies(df, drop_first=True)

df.to_csv("clean_loans.csv", index=False)

print("Clean dataset saved")
