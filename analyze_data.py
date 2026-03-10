import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:anolin%402006@localhost:5432/creditpath")

query = "SELECT * FROM loan_default"

df = pd.read_sql(query, engine)

print(df.head())
print(df.describe())