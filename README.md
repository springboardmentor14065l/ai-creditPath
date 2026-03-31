# AI-CreditPath
## Project Overview

CreditPath AI is a Machine Learning-based system designed to predict loan default risk using borrower financial data.
The project aims to assist financial institutions in making data-driven lending decisions by identifying high-risk applicants.

This system simulates real-world credit risk assessment used in:

- Banking systems
- Loan approval pipelines
- Credit scoring platforms

# Dataset Information

The dataset used in this project contains historical loan and borrower information, designed to analyze and predict loan default risk.
* Contains a mix of numerical and categorical features ,
Includes financial, demographic, and behavioral attributes

## Dataset Summary
- Total Records: 255,347
- Total Features: 18
- Target Variable: Default (0 = No Default, 1 = Default)

# Data Cleaning & Preprocessing

To ensure high-quality input data, the following steps were performed:

- Removed irrelevant and redundant features
- Handled missing values
- Converted percentage values (e.g., interest rate) into numeric format
- Standardized column names (lowercase, trimmed spaces)
- Corrected data types
- Performed basic outlier handling

## Dataset Variants

To maintain a clear workflow, two versions of the dataset were created:

## EDA Dataset (Without Encoding)

File: clean_loansfinal.csv

### Characteristics:
- Cleaned dataset
- Categorical variables retained in original form
- No encoding applied

### Purpose:

This dataset is used for Exploratory Data Analysis, where interpretability is crucial.

Keeping categorical values unchanged helps in:

- Better visualization (bar charts, distributions)
- Understanding category-wise trends
- Gaining meaningful insights into borrower behavior

## Model Dataset (With Encoding)
File: final_data_cleaned.csv

### Characteristics:
- Cleaned dataset
- Categorical variables encoded using:
- One-Hot Encoding
- Label Encoding
- Ready for ML model training

### Purpose:

Machine Learning models require numerical inputs.

Encoding ensures:

- Compatibility with algorithms
- Improved feature representation
- Better predictive performance
