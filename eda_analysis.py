import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/loan.csv")
# Display first rows
print("First 5 rows:")
print(df.head())

# Dataset shape
print("\nDataset Shape:")
print(df.shape)

# Column names
print("\nColumns:")
print(df.columns)

# Data types
print("\nData Types:")
print(df.dtypes)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Basic statistics
print("\nStatistical Summary:")
print(df.describe())

# Distribution of default status
print("\nDefault Status Distribution:")
print(df['loan_status'].value_counts())
# Plot default distribution
sns.countplot(x='loan_status', data=df)
plt.title("Loan Default Distribution")
plt.show()

# Income distribution
sns.histplot(df['annual_inc'], bins=30)
plt.title("Annual Income Distribution")
plt.show()



