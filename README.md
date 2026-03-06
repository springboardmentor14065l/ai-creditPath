# AI-CreditPath

## Dataset Information

This project uses the **Lending Club Loan Dataset**, which contains historical loan records including borrower financial information, loan details, and repayment status.

**Original Dataset Source:**  
https://www.kaggle.com/datasets/wordsforthewise/lending-club
The original dataset contains **millions of loan records and more than 150 features**.
After preprocessing and feature selection, the cleaned dataset used in this project contains:
- **391,164 rows**
- **72 processed features**

Due to **GitHub file size limitations**, the full cleaned dataset is not uploaded to this repository.  
Instead, a **sample dataset containing 20,000 rows** is provided to demonstrate the structure of the processed data.

---

## Data Preprocessing

The following preprocessing steps were applied:

1. **Feature Selection** – Selected relevant financial features from the original dataset.
2. **Loan Status Filtering** – Kept only *Fully Paid* and *Charged Off* loan records.
3. **Percentage Conversion** – Converted percentage columns (`int_rate`, `revol_util`) into numerical values.
4. **Employment Length Processing** – Converted employment length into numerical format.
5. **Missing Value Handling**
   - Median imputation for numerical features
   - `"Unknown"` category for categorical features
6. **Categorical Encoding** – Applied **one-hot encoding** to categorical variables.
7. **Final Dataset Generation** – Produced a cleaned dataset suitable for machine learning models.
