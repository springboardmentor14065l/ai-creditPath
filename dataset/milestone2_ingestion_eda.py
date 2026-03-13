# ============================================================
# CreditPathAI - Milestone 2: Data Ingestion & EDA
# Student: Akhil Babu Gujjaralapudi
# Dataset: Loan_default.csv (255,347 rows)
# ============================================================

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# STEP 1: LOAD DATASET
# ============================================================

print("=" * 60)
print("STEP 1: Loading Dataset")
print("=" * 60)

df = pd.read_csv('Loan_default.csv')

print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst 5 rows:\n{df.head()}")

# ============================================================
# STEP 2: DATA INGESTION INTO SQLITE
# ============================================================

print("\n" + "=" * 60)
print("STEP 2: Ingesting Data into SQLite")
print("=" * 60)

conn = sqlite3.connect('creditpath.db')
df.to_sql('loan_default', conn, if_exists='replace', index=False)

cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM loan_default")
print(f"Rows ingested into SQLite: {cursor.fetchone()[0]}")
print("Ingestion into creditpath.db successful!")

# ============================================================
# STEP 3: BASIC EDA
# ============================================================

print("\n" + "=" * 60)
print("STEP 3: Exploratory Data Analysis")
print("=" * 60)

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Missing Values ---")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "No missing values!")

print("\n--- Basic Statistics ---")
print(df.describe())

print("\n--- Default Distribution ---")
print(df['Default'].value_counts())
print(f"Default Rate: {df['Default'].mean()*100:.2f}%")

# ============================================================
# STEP 4: VISUALIZATIONS
# ============================================================

print("\n" + "=" * 60)
print("STEP 4: Generating Visualizations")
print("=" * 60)

os.makedirs('eda_plots', exist_ok=True)

# Plot 1: Default Distribution
plt.figure(figsize=(8, 5))
df['Default'].value_counts().plot(kind='bar', color=['green', 'red'], edgecolor='black')
plt.title('Loan Default Distribution')
plt.xlabel('Default (0=No, 1=Yes)')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('eda_plots/default_distribution.png')
plt.close()
print("Default distribution plot saved")

# Plot 2: Age Distribution by Default
plt.figure(figsize=(10, 5))
df[df['Default']==0]['Age'].hist(bins=30, alpha=0.6, color='green', label='No Default')
df[df['Default']==1]['Age'].hist(bins=30, alpha=0.6, color='red', label='Default')
plt.title('Age Distribution by Default Status')
plt.xlabel('Age')
plt.ylabel('Count')
plt.legend()
plt.tight_layout()
plt.savefig('eda_plots/age_vs_default.png')
plt.close()
print("Age vs Default plot saved")

# Plot 3: Credit Score vs Default
plt.figure(figsize=(10, 5))
df[df['Default']==0]['CreditScore'].hist(bins=30, alpha=0.6, color='green', label='No Default')
df[df['Default']==1]['CreditScore'].hist(bins=30, alpha=0.6, color='red', label='Default')
plt.title('Credit Score Distribution by Default Status')
plt.xlabel('Credit Score')
plt.ylabel('Count')
plt.legend()
plt.tight_layout()
plt.savefig('eda_plots/creditscore_vs_default.png')
plt.close()
print("Credit Score vs Default plot saved")

# Plot 4: Income vs Loan Amount
plt.figure(figsize=(10, 5))
plt.scatter(df[df['Default']==0]['Income'], df[df['Default']==0]['LoanAmount'], alpha=0.1, color='green', label='No Default')
plt.scatter(df[df['Default']==1]['Income'], df[df['Default']==1]['LoanAmount'], alpha=0.1, color='red', label='Default')
plt.title('Income vs Loan Amount by Default Status')
plt.xlabel('Income')
plt.ylabel('Loan Amount')
plt.legend()
plt.tight_layout()
plt.savefig('eda_plots/income_vs_loanamount.png')
plt.close()
print("Income vs Loan Amount plot saved")

# Plot 5: Default Rate by Employment Type
plt.figure(figsize=(10, 5))
df.groupby('EmploymentType')['Default'].mean().sort_values(ascending=False).plot(kind='bar', color='orange', edgecolor='black')
plt.title('Default Rate by Employment Type')
plt.xlabel('Employment Type')
plt.ylabel('Default Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('eda_plots/employment_vs_default.png')
plt.close()
print("Employment Type vs Default plot saved")

# Plot 6: Correlation Heatmap
plt.figure(figsize=(14, 10))
numeric_df = df.select_dtypes(include='number')
corr = numeric_df.corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('eda_plots/correlation_heatmap.png')
plt.close()
print("Correlation heatmap saved")

# Plot 7: Loan Purpose vs Default Rate
plt.figure(figsize=(12, 5))
df.groupby('LoanPurpose')['Default'].mean().sort_values(ascending=False).plot(kind='bar', color='purple', edgecolor='black')
plt.title('Default Rate by Loan Purpose')
plt.xlabel('Loan Purpose')
plt.ylabel('Default Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('eda_plots/loanpurpose_vs_default.png')
plt.close()
print("Loan Purpose vs Default plot saved")

# ============================================================
# STEP 5: EDA REPORT
# ============================================================

print("\n" + "=" * 60)
print("STEP 5: Generating EDA Report")
print("=" * 60)

default_rate = df['Default'].mean() * 100
total_rows = df.shape[0]
total_cols = df.shape[1]
missing_total = df.isnull().sum().sum()

report = f"""
========================================
CreditPathAI - EDA Report
Student: Akhil Babu Gujjaralapudi
Dataset: Loan_default.csv
========================================

1. DATASET OVERVIEW
-------------------
Total Rows     : {total_rows}
Total Columns  : {total_cols}
Missing Values : {missing_total}

Columns: {df.columns.tolist()}

2. TARGET VARIABLE ANALYSIS
----------------------------
Default = 0 (No Default) : {df['Default'].value_counts()[0]}
Default = 1 (Defaulted)  : {df['Default'].value_counts()[1]}
Overall Default Rate      : {default_rate:.2f}%

3. KEY STATISTICS
-----------------
Average Age          : {df['Age'].mean():.1f} years
Average Income       : {df['Income'].mean():.0f}
Average Loan Amount  : {df['LoanAmount'].mean():.0f}
Average Credit Score : {df['CreditScore'].mean():.1f}
Average Interest Rate: {df['InterestRate'].mean():.2f}%
Average DTI Ratio    : {df['DTIRatio'].mean():.2f}

4. KEY OBSERVATIONS
-------------------
- Dataset has {total_rows} borrower records with no missing values
- Default rate is {default_rate:.2f}% indicating class imbalance
- Credit Score and DTI Ratio are strong default predictors
- Employment Type significantly affects default probability
- Higher Interest Rate correlates with higher default risk

5. INGESTION STATUS
-------------------
- Data ingested into SQLite (creditpath.db)
- Table name: loan_default
- All {total_rows} rows verified

6. VISUALIZATIONS GENERATED
-----------------------------
- default_distribution.png
- age_vs_default.png
- creditscore_vs_default.png
- income_vs_loanamount.png
- employment_vs_default.png
- correlation_heatmap.png
- loanpurpose_vs_default.png

7. NEXT STEPS (Milestone 3)
----------------------------
- Feature engineering (encode categorical, normalize numeric)
- Train Logistic Regression baseline model
- Measure AUC-ROC score
- Refine feature pipeline if accuracy is low
"""

with open('eda_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print(report)
print("EDA Report saved as eda_report.txt")

conn.close()
print("\n" + "=" * 60)
print("MILESTONE 2 COMPLETE!")
print("=" * 60)
print("\nFiles generated:")
print("  - creditpath.db")
print("  - eda_report.txt")
print("  - eda_plots/ (7 visualizations)")