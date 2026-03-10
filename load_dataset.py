import pandas as pd
from sqlalchemy import create_engine

# connect to PostgreSQL
engine = create_engine("postgresql://postgres:anolin%402006@localhost:5432/creditpath")

# load dataset
df = pd.read_csv("Loan_default.csv")

# upload to PostgreSQL
df.to_sql("loan_default", engine, if_exists="replace", index=False)

print("Dataset uploaded successfully!")