import pandas as pd
import joblib
import numpy as np
import os
import time

# --- PATH CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')
MODELS_DIR = os.path.join(SCRIPT_DIR, '..', 'models')

def load_models():
    print("="*60)
    print("      INITIALIZING CREDITPATH AI: 3-WAY MODEL BATTLE")
    print("="*60)
    
    rf_path = os.path.join(MODELS_DIR, 'credit_path_model.pkl')
    xgb_path = os.path.join(MODELS_DIR, 'best_xgboost_model.pkl')
    lgb_path = os.path.join(MODELS_DIR, 'best_lightgbm_model.pkl')
    scaler_path = os.path.join(MODELS_DIR, 'scaler.joblib')

    # Load Scaler
    scaler = joblib.load(scaler_path)
    
    # Load XGBoost (Tuned)
    print(f"Loading Tuned XGBoost... (Size: 0.23 MB)")
    xgb_model = joblib.load(xgb_path)

    # Load LightGBM (Baseline)
    print(f"Loading Baseline LightGBM... (Size: 0.70 MB)")
    lgb_model = joblib.load(lgb_path)
    
    # Load Random Forest (Baseline)
    rf_model = None
    if os.path.exists(rf_path):
        print(f"Loading Baseline Random Forest... (Size: 370.42 MB)")
        start_time = time.time()
        rf_model = joblib.load(rf_path)
        print(f"RF Loaded in {time.time() - start_time:.2f}s")
    else:
        print("Note: Baseline Random Forest model not found locally.")

    return rf_model, xgb_model, lgb_model, scaler

def compare_predictions():
    rf_model, xgb_model, lgb_model, scaler = load_models()
    
    print("\n" + "="*70)
    print("      REAL-TIME RISK ASSESSMENT: RF vs XGB vs LightGBM")
    print("="*70)
    
    try:
        # Collect Raw Inputs
        age = int(input("Enter Age (18-70): "))
        income = float(input("Enter Annual Income ($): "))
        loan_amt = float(input("Enter Loan Amount ($): "))
        credit_score = int(input("Enter Credit Score (300-850): "))
        months_emp = int(input("Enter Months Employed: "))
        num_credit_lines = int(input("Enter Number of Credit Lines: "))
        interest = float(input("Enter Interest Rate (%): "))
        loan_term = int(input("Enter Loan Term (months): "))
        dti = float(input("Enter Debt-to-Income Ratio (0.1 - 1.0): "))
        
        print("\nEducation: 1.High School, 2.Bachelor's, 3.Master's, 4.PhD")
        edu_choice = input("Choice (1-4): ")
        
        print("\nEmployment: 1.Full-time, 2.Part-time, 3.Self-employed, 4.Unemployed")
        emp_choice = input("Choice (1-4): ")

        print("\nMarital Status: 1.Single, 2.Married, 3.Divorced")
        mar_choice = input("Choice (1-3): ")

        # Feature Engineering
        feature_names = xgb_model.feature_names_in_
        user_input = pd.DataFrame(np.zeros((1, len(feature_names))), columns=feature_names)
        
        user_input['age'] = age
        user_input['income'] = income
        user_input['loan_amount'] = loan_amt
        user_input['credit_score'] = credit_score
        user_input['months_employed'] = months_emp
        user_input['num_credit_lines'] = num_credit_lines
        user_input['interest_rate'] = interest
        user_input['loan_term'] = loan_term
        user_input['dti_ratio'] = dti
        
        user_input['loan_to_income'] = loan_amt / income
        user_input['credit_utilization'] = loan_amt / num_credit_lines
        user_input['interest_burden'] = loan_amt * interest
        user_input['employment_stability'] = months_emp / age
        user_input['high_dti_flag'] = 1 if dti > 0.5 else 0
        user_input['log_income'] = np.log1p(income)
        user_input['income_loan_interaction'] = income * loan_amt
        
        if edu_choice == '1': user_input['education_High School'] = 1
        elif edu_choice == '3': user_input["education_Master's"] = 1
        elif edu_choice == '4': user_input['education_PhD'] = 1
        
        if emp_choice == '2': user_input['employmenttype_Part-time'] = 1
        elif emp_choice == '3': user_input['employmenttype_Self-employed'] = 1
        elif emp_choice == '4': user_input['employmenttype_Unemployed'] = 1

        if mar_choice == '1': user_input['maritalstatus_Single'] = 1
        elif mar_choice == '2': user_input['maritalstatus_Married'] = 1

        if 600 < credit_score <= 700: user_input['credit_score_bucket_Average'] = 1
        elif 700 < credit_score <= 800: user_input['credit_score_bucket_Good'] = 1
        elif credit_score > 800: user_input['credit_score_bucket_Excellent'] = 1

        user_input['hascosigner_Yes'] = 1
        user_input['loanpurpose_Education'] = 1
        
        # Scaling
        cols_to_scale = ['income', 'loan_amount', 'credit_score', 'loan_to_income', 'credit_utilization', 'interest_burden', 'employment_stability', 'log_income', 'income_loan_interaction']
        user_input_scaled = user_input.copy()
        user_input_scaled[cols_to_scale] = scaler.transform(user_input[cols_to_scale])
        
        # --- PREDICTIONS ---
        xgb_prob = xgb_model.predict_proba(user_input_scaled)[0][1]
        lgb_prob = lgb_model.predict_proba(user_input_scaled)[0][1]
        rf_prob = rf_model.predict_proba(user_input_scaled)[0][1] if rf_model else 0

        # --- COMPARATIVE OUTPUT ---
        print("\n" + "="*80)
        print(f"{'METRIC':<20} | {'RF (BASELINE)':<15} | {'XGB (TUNED)':<15} | {'LGBM (BASELINE)':<15}")
        print("-" * 80)
        print(f"{'File Size':<20} | {'370.42 MB':<15} | {'0.23 MB':<15} | {'0.70 MB':<15}")
        print(f"{'AUC-ROC':<20} | {'0.7341':<15} | {'0.7603':<15} | {'0.7580':<15}")
        print("-" * 80)
        
        rf_res = ("APPROVED" if rf_prob < 0.35 else "DENIED") if rf_model else "N/A"
        xgb_res = "APPROVED" if xgb_prob < 0.25 else "DENIED"
        lgb_res = "APPROVED" if lgb_prob < 0.25 else "DENIED"
        
        rf_prob_str = f"{rf_prob*100:>13.2f}%" if rf_model else f"{'N/A':>15}"
        
        print(f"{'Risk Probability':<20} | {rf_prob_str} | {xgb_prob*100:>13.2f}% | {lgb_prob*100:>13.2f}%")
        print(f"{'Final Decision':<20} | {rf_res:>15} | {xgb_res:>15} | {lgb_res:>15}")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n[Error] {e}")

if __name__ == "__main__":
    compare_predictions()
