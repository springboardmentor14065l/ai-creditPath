import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv(r"C:\Users\MS Shamanth\Downloads\Loan_Default.csv")

print("Rows in CSV:", len(df))

engine = create_engine("postgresql://postgres:Sham%408029@localhost:5432/creditpath")

df.to_sql("loan_default", engine, if_exists="replace", index=False)

print("Data uploaded successfully")
