import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:password@localhost:5432/creditpath")

# Show first rows
df = pd.read_sql("SELECT * FROM loans LIMIT 5", engine)
print(df)

# Count rows
count = pd.read_sql("SELECT COUNT(*) FROM loans", engine)
print(count)