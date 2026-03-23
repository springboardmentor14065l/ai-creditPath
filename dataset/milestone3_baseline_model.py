# ============================================================
# CreditPathAI – Milestone 3: Baseline Model (Logistic Regression)
# Student : Akhil Babu Gujjaralapudi
# Follows : Baseline Model Handout (mentor guide)
# Input   : final_features.csv
# Metric  : AUC-ROC
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection   import train_test_split
from sklearn.preprocessing     import StandardScaler
from sklearn.linear_model      import LogisticRegression
from sklearn.metrics           import (
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, ConfusionMatrixDisplay
)

import os
os.makedirs('model_plots', exist_ok=True)

# ============================================================
# STEP 1: LOAD DATASET
# ============================================================
print("=" * 60)
print("STEP 1: Load Dataset (final_features.csv)")
print("=" * 60)

df = pd.read_csv('final_features.csv')

print(f"Shape  : {df.shape}")
print(f"Target : default_status")
print(f"Class distribution:\n{df['default_status'].value_counts()}")

# ============================================================
# STEP 2: DEFINE FEATURES AND TARGET
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: Define Features (X) and Target (y)")
print("=" * 60)

X = df.drop('default_status', axis=1)
y = df['default_status']

print(f"X shape : {X.shape}")
print(f"y shape : {y.shape}")
print(f"Features: {X.columns.tolist()}")

# ============================================================
# STEP 3: TRAIN-TEST SPLIT
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: Train-Test Split (80/20)")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training samples : {X_train.shape[0]}")
print(f"Testing samples  : {X_test.shape[0]}")

# ============================================================
# STEP 4: SCALING  ← MANDATORY
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: Feature Scaling (StandardScaler) — MANDATORY")
print("=" * 60)

scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

print("✅ StandardScaler applied (fit on train, transform on test)")

# ============================================================
# STEP 5: TRAIN LOGISTIC REGRESSION MODEL
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: Train Logistic Regression Model")
print("=" * 60)

model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

print("✅ Model trained with class_weight='balanced' (handles imbalance)")

# ============================================================
# STEP 6: PREDICTIONS
# ============================================================
print("\n" + "=" * 60)
print("STEP 6: Generate Predictions")
print("=" * 60)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print(f"Predicted 0 (No Default): {(y_pred == 0).sum()}")
print(f"Predicted 1 (Default)   : {(y_pred == 1).sum()}")

# ============================================================
# STEP 7: EVALUATION — AUC-ROC  ← PRIMARY METRIC
# ============================================================
print("\n" + "=" * 60)
print("STEP 7: Evaluation — AUC-ROC (PRIMARY METRIC)")
print("=" * 60)

auc = roc_auc_score(y_test, y_prob)
print(f"\n🎯 AUC-ROC Score : {auc:.4f}")

if auc >= 0.80:
    print("🏆 Excellent! AUC > 0.80")
elif auc >= 0.75:
    print("✅ Very Good! AUC > 0.75")
elif auc >= 0.70:
    print("✅ Good! AUC > 0.70")
else:
    print("⚠ AUC < 0.65 — Improve Feature Engineering")

print("\n--- Confusion Matrix ---")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\n--- Classification Report ---")
print(classification_report(y_test, y_pred, target_names=['No Default', 'Default']))

# ============================================================
# STEP 8: FEATURE INTERPRETATION (COEFFICIENTS)
# ============================================================
print("\n" + "=" * 60)
print("STEP 8: Feature Interpretation (Coefficients)")
print("=" * 60)

feature_names = df.drop('default_status', axis=1).columns

coeff = pd.DataFrame({
    'Feature'    : feature_names,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)

print("\n--- Top Features INCREASING Default Risk (Positive Coefficient) ---")
print(coeff.head(10).to_string(index=False))

print("\n--- Top Features DECREASING Default Risk (Negative Coefficient) ---")
print(coeff.tail(10).to_string(index=False))

# ============================================================
# PLOTS
# ============================================================
print("\n" + "=" * 60)
print("Generating Plots")
print("=" * 60)

# Plot 1: ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'AUC = {auc:.4f}')
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
plt.title('ROC Curve – Logistic Regression')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('model_plots/roc_curve.png')
plt.close()
print("Plot saved: roc_curve.png")

# Plot 2: Confusion Matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=['No Default', 'Default'])
fig, ax = plt.subplots(figsize=(8, 6))
disp.plot(ax=ax, cmap='Blues', colorbar=False)
plt.title('Confusion Matrix – Logistic Regression')
plt.tight_layout()
plt.savefig('model_plots/confusion_matrix.png')
plt.close()
print("Plot saved: confusion_matrix.png")

# Plot 3: Top 15 Feature Coefficients
top15 = pd.concat([coeff.head(8), coeff.tail(7)])
plt.figure(figsize=(12, 7))
colors = ['red' if c > 0 else 'green' for c in top15['Coefficient']]
plt.barh(top15['Feature'], top15['Coefficient'], color=colors, edgecolor='black')
plt.axvline(0, color='black', linewidth=0.8)
plt.title('Top Feature Coefficients – Logistic Regression\n(Red = Increases Risk | Green = Decreases Risk)')
plt.xlabel('Coefficient Value')
plt.tight_layout()
plt.savefig('model_plots/feature_coefficients.png')
plt.close()
print("Plot saved: feature_coefficients.png")

# ============================================================
# STEP 9: MODEL REPORT
# ============================================================
report_text = f"""
========================================
CreditPathAI – Milestone 3: Baseline Model Report
Student : Akhil Babu Gujjaralapudi
Model   : Logistic Regression
========================================

1. MODEL CONFIGURATION
-----------------------
Algorithm      : Logistic Regression
Max Iterations : 1000
Class Weight   : balanced (handles class imbalance)
Scaling        : StandardScaler (mandatory)
Train/Test     : 80/20 split (stratified)

2. EVALUATION RESULTS
----------------------
AUC-ROC Score  : {auc:.4f}

Confusion Matrix:
{cm}

3. TOP FEATURES INCREASING DEFAULT RISK
-----------------------------------------
{coeff.head(5).to_string(index=False)}

4. TOP FEATURES DECREASING DEFAULT RISK
-----------------------------------------
{coeff.tail(5).to_string(index=False)}

5. KEY OBSERVATIONS
--------------------
- AUC-ROC of {auc:.4f} indicates the model's ability to distinguish defaulters
- class_weight='balanced' used to handle 11.61% class imbalance
- Logistic Regression provides interpretable coefficients for each feature
- Top risk factors align with EDA findings (credit score, DTI, interest rate)

6. NEXT STEPS (Milestone 4)
-----------------------------
- Train XGBoost model
- Train LightGBM model
- Compare AUC-ROC across all three models
- Hyperparameter tuning using GridSearchCV

7. PLOTS GENERATED (model_plots/)
-----------------------------------
- roc_curve.png
- confusion_matrix.png
- feature_coefficients.png
"""

with open('milestone3_report.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)

print(report_text)
print("Report saved: milestone3_report.txt")

print("\n" + "=" * 60)
print("✅ MILESTONE 3 COMPLETE!")
print("=" * 60)
print("\nFiles generated:")
print("  - final_features.csv (from feature engineering)")
print("  - milestone3_report.txt")
print("  - model_plots/roc_curve.png")
print("  - model_plots/confusion_matrix.png")
print("  - model_plots/feature_coefficients.png")
