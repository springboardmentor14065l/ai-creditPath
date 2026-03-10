import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Step 1 – Load Clean Dataset
df = pd.read_csv("clean_loans.csv")

print("Dataset Loaded Successfully\n")

# Step 2 – View First Rows
print("First 5 Records:")
print(df.head())

# Step 3 – Dataset Information
print("\nDataset Info:")
print(df.info())

# Step 4 – Statistical Summary
print("\nStatistical Summary:")
print(df.describe())

# Step 5 – Check Loan Default Distribution
print("\nLoan Default Distribution:")
print(df['default'].value_counts())

sns.countplot(x='default', data=df)
plt.title("Loan Default Distribution")
plt.show()

# Step 6 – Correlation Matrix
plt.figure(figsize=(12,8))
sns.heatmap(df.corr(), cmap="coolwarm")
plt.title("Feature Correlation Heatmap")
plt.show()

# Step 7 – Income Distribution
plt.figure(figsize=(6,4))
sns.histplot(df['income'], bins=30)
plt.title("Income Distribution")
plt.show()

# Step 8 – Credit Score Distribution
plt.figure(figsize=(6,4))
sns.histplot(df['creditscore'], bins=30)
plt.title("Credit Score Distribution")
plt.show()

# Step 9 – Loan Amount Distribution
plt.figure(figsize=(6,4))
sns.histplot(df['loanamount'], bins=30)
plt.title("Loan Amount Distribution")
plt.show()

print("\nEDA Completed Successfully")