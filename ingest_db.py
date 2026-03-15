import pandas as pd
from sqlalchemy import create_engine

# Database connection details
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "creditpath"

# Create connection
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("Connecting to PostgreSQL...")

# Load dataset
df = pd.read_csv("data/loan.csv", low_memory=False)

print("Dataset loaded successfully!")
print("Total rows:", len(df))

# Upload dataset to PostgreSQL
df.to_sql("loans", engine, if_exists="replace", index=False)

print("✅ Data successfully ingested into PostgreSQL!")