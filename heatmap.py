import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine("postgresql://postgres:malleswari%40123@localhost:5432/creditpath")

# Load dataset
df = pd.read_sql("SELECT * FROM loan_default", engine)

print("Dataset Loaded Successfully")

# Convert possible numeric columns to numbers
numeric_cols = [
    "age","income","loan_amount","credit_score",
    "months_employed","num_credit_lines",
    "interest_rate","loan_term","dti_ratio","default_status"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Take sample
df_sample = df[numeric_cols].sample(5000)

# Correlation matrix
corr_matrix = df_sample.corr()

# Plot heatmap
plt.figure(figsize=(10,6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()