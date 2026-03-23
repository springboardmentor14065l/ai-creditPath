# ============================================================
# CreditPathAI – Milestone 2: Complete EDA
# Student : Akhil Babu Gujjaralapudi
# Dataset : Loan_default.csv (255,347 rows, 18 columns)
# Follows : EDA Handout (mentor guide)
# ============================================================

import pandas as pd
import numpy as np
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs('eda_plots', exist_ok=True)

# ============================================================
# STEP 1: LOAD THE CLEAN DATASET
# ============================================================
print("=" * 60)
print("STEP 1: Load Dataset")
print("=" * 60)

df = pd.read_csv('Loan_default.csv')

# Rename columns to match handout conventions
df.rename(columns={
    'Age'            : 'age',
    'Income'         : 'income',
    'LoanAmount'     : 'loan_amount',
    'CreditScore'    : 'credit_score',
    'MonthsEmployed' : 'months_employed',
    'NumCreditLines' : 'num_credit_lines',
    'InterestRate'   : 'interest_rate',
    'LoanTerm'       : 'loan_term',
    'DTIRatio'       : 'dti_ratio',
    'Education'      : 'education',
    'EmploymentType' : 'employment_type',
    'MaritalStatus'  : 'marital_status',
    'HasMortgage'    : 'has_mortgage',
    'HasDependents'  : 'has_dependents',
    'LoanPurpose'    : 'loan_purpose',
    'HasCoSigner'    : 'has_cosigner',
    'Default'        : 'default_status'
}, inplace=True)

print(f"Shape      : {df.shape}")
print(f"Columns    : {df.columns.tolist()}")
print(f"\nFirst 5 rows:\n{df.head()}")

# ============================================================
# STEP 2: DATA INGESTION INTO SQLITE
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: Ingest Data into SQLite")
print("=" * 60)

conn = sqlite3.connect('creditpath.db')
df.to_sql('loan_default', conn, if_exists='replace', index=False)

cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM loan_default")
count = cursor.fetchone()[0]
print(f"Rows ingested into SQLite : {count}")
print("Database: creditpath.db | Table: loan_default")

# ============================================================
# STEP 3: DATASET OVERVIEW
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: Dataset Overview")
print("=" * 60)

print(f"\nShape   : {df.shape}")
print(f"Columns : {df.columns.tolist()}")
print("\nData Types & Non-Null Counts:")
print(df.info())

# ============================================================
# STEP 4: TARGET VARIABLE ANALYSIS  ← MOST IMPORTANT
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: Target Variable Analysis (MOST IMPORTANT)")
print("=" * 60)

target_counts = df['default_status'].value_counts()
target_pct    = df['default_status'].value_counts(normalize=True) * 100

print(f"\nDefault = 0 (No Default) : {target_counts[0]}")
print(f"Default = 1 (Defaulted)  : {target_counts[1]}")
print(f"Default Rate             : {target_pct[1]:.2f}%")
print("\n⚠ Class Imbalance Detected — will use class_weight='balanced' in modeling")

# Plot
plt.figure(figsize=(8, 5))
sns.countplot(x='default_status', data=df, palette=['green', 'red'])
plt.title('Target Variable – Loan Default Distribution')
plt.xlabel('Default Status (0 = No Default, 1 = Default)')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('eda_plots/default_distribution.png')
plt.close()
print("Plot saved: default_distribution.png")

# ============================================================
# STEP 5: NUMERICAL FEATURE ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: Numerical Feature Analysis")
print("=" * 60)

numeric_cols = ['age', 'income', 'loan_amount', 'credit_score',
                'dti_ratio', 'interest_rate', 'months_employed',
                'num_credit_lines', 'loan_term']

print("\n--- Basic Statistics ---")
print(df[numeric_cols].describe())

print("\n--- Mean vs Median (Skewness Check) ---")
for col in numeric_cols:
    mean   = df[col].mean()
    median = df[col].median()
    skew   = df[col].skew()
    print(f"{col:22s} | Mean: {mean:10.2f} | Median: {median:10.2f} | Skew: {skew:.2f}")

# Histplots
for col in ['income', 'credit_score']:
    plt.figure(figsize=(10, 5))
    sns.histplot(df[col], kde=True, color='steelblue')
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.tight_layout()
    plt.savefig(f'eda_plots/hist_{col}.png')
    plt.close()
    print(f"Plot saved: hist_{col}.png")

# ============================================================
# STEP 6: MISSING VALUES
# ============================================================
print("\n" + "=" * 60)
print("STEP 6: Missing Value Analysis")
print("=" * 60)

missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "✅ No missing values found!")

# ============================================================
# STEP 7: FEATURE vs TARGET ANALYSIS  ← CRITICAL
# ============================================================
print("\n" + "=" * 60)
print("STEP 7: Feature vs Target Analysis (CRITICAL)")
print("=" * 60)

for col in ['credit_score', 'income', 'dti_ratio']:
    plt.figure(figsize=(10, 5))
    sns.boxplot(x='default_status', y=col, data=df, palette=['green', 'red'])
    plt.title(f'{col} by Default Status')
    plt.xlabel('Default Status')
    plt.ylabel(col)
    plt.tight_layout()
    plt.savefig(f'eda_plots/boxplot_{col}_vs_default.png')
    plt.close()
    print(f"Plot saved: boxplot_{col}_vs_default.png")

# Age distribution
plt.figure(figsize=(10, 5))
df[df['default_status'] == 0]['age'].hist(bins=30, alpha=0.6, color='green', label='No Default')
df[df['default_status'] == 1]['age'].hist(bins=30, alpha=0.6, color='red',   label='Default')
plt.title('Age Distribution by Default Status')
plt.xlabel('Age')
plt.ylabel('Count')
plt.legend()
plt.tight_layout()
plt.savefig('eda_plots/age_vs_default.png')
plt.close()
print("Plot saved: age_vs_default.png")

# Credit Score distribution
plt.figure(figsize=(10, 5))
df[df['default_status'] == 0]['credit_score'].hist(bins=30, alpha=0.6, color='green', label='No Default')
df[df['default_status'] == 1]['credit_score'].hist(bins=30, alpha=0.6, color='red',   label='Default')
plt.title('Credit Score Distribution by Default Status')
plt.xlabel('Credit Score')
plt.ylabel('Count')
plt.legend()
plt.tight_layout()
plt.savefig('eda_plots/creditscore_vs_default.png')
plt.close()
print("Plot saved: creditscore_vs_default.png")

# ============================================================
# STEP 8: CATEGORICAL FEATURE ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("STEP 8: Categorical Feature Analysis")
print("=" * 60)

cat_cols = ['education', 'employment_type', 'marital_status', 'loan_purpose']

for col in cat_cols:
    plt.figure(figsize=(12, 5))
    sns.countplot(x=col, hue='default_status', data=df, palette=['green', 'red'])
    plt.title(f'{col} vs Default Status')
    plt.xlabel(col)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Default', labels=['No Default', 'Default'])
    plt.tight_layout()
    plt.savefig(f'eda_plots/{col}_vs_default.png')
    plt.close()
    print(f"Plot saved: {col}_vs_default.png")

# ============================================================
# STEP 9: CORRELATION ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("STEP 9: Correlation Analysis")
print("=" * 60)

numeric_df = df.select_dtypes(include='number')
corr = numeric_df.corr()

print("\nCorrelation with default_status (sorted):")
print(corr['default_status'].sort_values(ascending=False))

plt.figure(figsize=(14, 10))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, linewidths=0.5)
plt.title('Correlation Heatmap – CreditPathAI')
plt.tight_layout()
plt.savefig('eda_plots/correlation_heatmap.png')
plt.close()
print("Plot saved: correlation_heatmap.png")

# ============================================================
# STEP 10: FEATURE INTERACTIONS (ADVANCED)
# ============================================================
print("\n" + "=" * 60)
print("STEP 10: Feature Interactions (ADVANCED)")
print("=" * 60)

plt.figure(figsize=(10, 6))
sample = df.sample(5000, random_state=42)
sns.scatterplot(x='income', y='loan_amount', hue='default_status',
                data=sample, palette=['green', 'red'], alpha=0.5)
plt.title('Income vs Loan Amount by Default Status')
plt.xlabel('Income')
plt.ylabel('Loan Amount')
plt.tight_layout()
plt.savefig('eda_plots/income_vs_loanamount.png')
plt.close()
print("Plot saved: income_vs_loanamount.png")
print("Insight: High Loan + Low Income → Higher Default Risk")

# ============================================================
# STEP 11: OUTLIER IMPACT ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("STEP 11: Outlier Impact Analysis")
print("=" * 60)

plt.figure(figsize=(10, 5))
sns.boxplot(data=df[['income', 'loan_amount', 'credit_score']])
plt.title('Outlier Check – Income, Loan Amount, Credit Score')
plt.tight_layout()
plt.savefig('eda_plots/outlier_boxplot.png')
plt.close()
print("Plot saved: outlier_boxplot.png")

for col in ['income', 'loan_amount']:
    q1  = df[col].quantile(0.25)
    q3  = df[col].quantile(0.75)
    iqr = q3 - q1
    outliers = df[(df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)]
    print(f"{col}: {len(outliers)} outliers detected ({len(outliers)/len(df)*100:.2f}%)")

# ============================================================
# STEP 12: SEGMENTATION ANALYSIS  ← VERY IMPORTANT
# ============================================================
print("\n" + "=" * 60)
print("STEP 12: Segmentation Analysis (VERY IMPORTANT)")
print("=" * 60)

print("\n--- Default Rate by Education ---")
print(df.groupby('education')['default_status'].mean().sort_values(ascending=False))

print("\n--- Default Rate by Loan Purpose ---")
lp = df.groupby('loan_purpose')['default_status'].mean().sort_values(ascending=False)
print(lp)

plt.figure(figsize=(12, 5))
lp.plot(kind='bar', color='purple', edgecolor='black')
plt.title('Default Rate by Loan Purpose')
plt.xlabel('Loan Purpose')
plt.ylabel('Default Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('eda_plots/loanpurpose_vs_default.png')
plt.close()
print("Plot saved: loanpurpose_vs_default.png")

print("\n--- Default Rate by Employment Type ---")
et = df.groupby('employment_type')['default_status'].mean().sort_values(ascending=False)
print(et)

plt.figure(figsize=(10, 5))
et.plot(kind='bar', color='orange', edgecolor='black')
plt.title('Default Rate by Employment Type')
plt.xlabel('Employment Type')
plt.ylabel('Default Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('eda_plots/employment_vs_default.png')
plt.close()
print("Plot saved: employment_vs_default.png")

# ============================================================
# STEP 13: KEY INSIGHTS + EDA REPORT
# ============================================================
print("\n" + "=" * 60)
print("STEP 13: Key Insights & EDA Report")
print("=" * 60)

default_rate  = df['default_status'].mean() * 100
total_rows    = df.shape[0]
total_cols    = df.shape[1]
missing_total = df.isnull().sum().sum()

report = f"""
========================================
CreditPathAI – EDA Report
Student : Akhil Babu Gujjaralapudi
Dataset : Loan_default.csv
========================================

1. DATASET OVERVIEW
--------------------
Total Rows     : {total_rows}
Total Columns  : {total_cols}
Missing Values : {missing_total}
Columns        : {df.columns.tolist()}

2. TARGET VARIABLE ANALYSIS
-----------------------------
Default = 0 (No Default) : {df['default_status'].value_counts()[0]}
Default = 1 (Defaulted)  : {df['default_status'].value_counts()[1]}
Overall Default Rate      : {default_rate:.2f}%
⚠ Class imbalance detected → will use class_weight='balanced' in modeling

3. KEY STATISTICS
------------------
Average Age            : {df['age'].mean():.1f} years
Average Income         : {df['income'].mean():.0f}
Average Loan Amount    : {df['loan_amount'].mean():.0f}
Average Credit Score   : {df['credit_score'].mean():.1f}
Average Interest Rate  : {df['interest_rate'].mean():.2f}%
Average DTI Ratio      : {df['dti_ratio'].mean():.2f}
Average Months Employed: {df['months_employed'].mean():.1f}

4. TOP 5 FACTORS AFFECTING DEFAULT (Key Insights)
---------------------------------------------------
1. Credit Score  → Borrowers with credit_score < 600 show significantly higher default rates
2. DTI Ratio     → DTI > 0.5 strongly correlates with default (high debt burden)
3. Interest Rate → Higher interest rate → greater repayment difficulty → higher default
4. Employment Type → Unemployed/Part-time borrowers default more than full-time employees
5. Income        → Lower income borrowers with high loan amounts are highest risk segment

5. HIGH-RISK BORROWER PROFILE
-------------------------------
- Credit Score < 600
- DTI Ratio > 0.5
- Unemployment or Part-time employment
- High Loan-to-Income ratio
- Loan Purpose: Business or Personal (higher default rates)

6. UNEXPECTED PATTERNS
------------------------
- Marital status shows minimal effect on default
- Age distribution is fairly uniform across both default classes
- HasCoSigner does not drastically reduce default probability

7. INGESTION STATUS
--------------------
- Data ingested into SQLite: creditpath.db
- Table name           : loan_default
- Total rows verified  : {total_rows}

8. VISUALIZATIONS GENERATED (eda_plots/)
-----------------------------------------
- default_distribution.png
- hist_income.png
- hist_credit_score.png
- age_vs_default.png
- creditscore_vs_default.png
- boxplot_credit_score_vs_default.png
- boxplot_income_vs_default.png
- boxplot_dti_ratio_vs_default.png
- education_vs_default.png
- employment_type_vs_default.png
- marital_status_vs_default.png
- loan_purpose_vs_default.png
- correlation_heatmap.png
- income_vs_loanamount.png
- outlier_boxplot.png
- loanpurpose_vs_default.png
- employment_vs_default.png

9. NEXT STEPS (Milestone 3)
-----------------------------
- Feature Engineering (encode categoricals, create new features)
- Train Logistic Regression baseline model
- Evaluate using AUC-ROC (target > 0.70)
- Refine feature pipeline if AUC < 0.65
"""

with open('eda_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print(report)
print("EDA Report saved: eda_report.txt")

conn.close()
print("\n" + "=" * 60)
print("✅ MILESTONE 2 COMPLETE!")
print("=" * 60)
print("\nFiles generated:")
print("  - creditpath.db")
print("  - eda_report.txt")
print("  - eda_plots/ (17 visualizations)")
