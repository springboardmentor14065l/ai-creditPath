import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql://postgres:root@localhost:5432/creditpath_db"
)

# Load CSV
df = pd.read_csv("data/raw/loan_default.csv")

# Insert into PostgreSQL
df.to_sql(
    "loan_data",
    engine,
    if_exists="replace",
    index=False
)

print("Data successfully ingested into PostgreSQL")