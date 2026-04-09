import numpy as np

def feature_engineering(X):
    X = X.copy()

    X["loan_income_ratio"] = X["loanamount"] / (X["income"] + 1)
    X["credit_income_ratio"] = X["creditscore"] / (X["income"] + 1)

    X["loan_credit_interaction"] = X["loanamount"] * (700 - X["creditscore"])

    X["high_loan_flag"] = (X["loanamount"] > X["income"]).astype(int)
    X["low_credit_flag"] = (X["creditscore"] < 600).astype(int)

    if "dtiratio" in X.columns:
        X["loan_dti_interaction"] = X["loanamount"] * X["dtiratio"]
        X["high_dti_flag"] = (X["dtiratio"] > 0.4).astype(int)

    return X