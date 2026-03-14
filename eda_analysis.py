import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 1️⃣ Connect to PostgreSQL
engine = create_engine("postgresql://postgres:malleswari%40123@localhost:5432/creditpath")

# 2️⃣ Load dataset
df = pd.read_sql("SELECT * FROM loan_default", engine)

print("Dataset Loaded Successfully\n")

# 3️⃣ View dataset
print("First 5 rows:")
print(df.head())

# 4️⃣ Dataset information
print("\nDataset Info:")
print(df.info())

# 5️⃣ Statistical summary
print("\nStatistical Summary:")
print(df.describe())

# 6️⃣ Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 7️⃣ Use sample for faster graphs
df_sample = df.sample(5000)

# -------------------------------
# GRAPH 1 – Loan Default Distribution
# -------------------------------
plt.figure(figsize=(6,4))
sns.countplot(x="default_status", data=df_sample)
plt.title("Loan Default Distribution")
plt.show()

# -------------------------------
# GRAPH 2 – Income Distribution
# -------------------------------
plt.figure(figsize=(6,4))
sns.histplot(df_sample["income"], bins=30, kde=True)
plt.title("Income Distribution")
plt.show()

# -------------------------------
# GRAPH 3 – Credit Score Distribution
# -------------------------------
plt.figure(figsize=(6,4))
sns.histplot(df_sample["credit_score"], bins=30, kde=True)
plt.title("Credit Score Distribution")
plt.show()

# -------------------------------
# GRAPH 4 – Loan Amount Distribution
# -------------------------------
plt.figure(figsize=(6,4))
sns.histplot(df_sample["loan_amount"], bins=30, kde=True)
plt.title("Loan Amount Distribution")
plt.show()

# -------------------------------
# GRAPH 5 – Income vs Default
# -------------------------------
plt.figure(figsize=(6,4))
sns.boxplot(x="default_status", y="income", data=df_sample)
plt.title("Income vs Loan Default")
plt.show()

# -------------------------------
# GRAPH 6 – Credit Score vs Default
# -------------------------------
plt.figure(figsize=(6,4))
sns.boxplot(x="default_status", y="credit_score", data=df_sample)
plt.title("Credit Score vs Loan Default")
plt.show()

# -------------------------------
# GRAPH 7 – Loan Purpose Distribution
# -------------------------------
plt.figure(figsize=(7,4))
sns.countplot(x="loan_purpose", data=df_sample)
plt.title("Loan Purpose Distribution")
plt.xticks(rotation=45)
plt.show()

# -------------------------------
# Correlation Heatmap
# -------------------------------

# Select only numeric columns
numeric_df = df_sample.select_dtypes(include=['int64', 'float64'])

# Compute correlation
corr_matrix = numeric_df.corr()

# Plot heatmap
plt.figure(figsize=(10,6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# -------------------------------
# DATA CLEANING
# -------------------------------

# Remove unnecessary column
df = df.drop(columns=["loan_id"])

# Convert categorical variables
df = pd.get_dummies(df, drop_first=True)

# Save cleaned dataset
df.to_csv("clean_loans.csv", index=False)

print("\nClean dataset saved as clean_loans.csv")