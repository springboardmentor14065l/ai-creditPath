import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report, roc_curve, ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import os

os.makedirs('model_plots', exist_ok=True)

df = pd.read_csv('final_features.csv')

print(f"Shape: {df.shape}")
print(f"Target distribution:\n{df['default_status'].value_counts()}")

X = df.drop('default_status', axis=1)
y = df['default_status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
lr.fit(X_train_scaled, y_train)
y_prob_lr = lr.predict_proba(X_test_scaled)[:, 1]
auc_lr = roc_auc_score(y_test, y_prob_lr)
print(f"\nLogistic Regression AUC: {auc_lr:.4f}")

xgb = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='logloss',
    verbosity=0
)
xgb.fit(X_train, y_train)
y_prob_xgb = xgb.predict_proba(X_test)[:, 1]
auc_xgb = roc_auc_score(y_test, y_prob_xgb)
print(f"XGBoost AUC: {auc_xgb:.4f}")

lgbm = LGBMClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    verbose=-1
)
lgbm.fit(X_train, y_train)
y_prob_lgbm = lgbm.predict_proba(X_test)[:, 1]
auc_lgbm = roc_auc_score(y_test, y_prob_lgbm)
print(f"LightGBM AUC: {auc_lgbm:.4f}")

param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1],
    'n_estimators': [100, 200]
}

grid = GridSearchCV(
    XGBClassifier(random_state=42, eval_metric='logloss', verbosity=0),
    param_grid,
    scoring='roc_auc',
    cv=3,
    n_jobs=-1
)
grid.fit(X_train, y_train)

best_model = grid.best_estimator_
y_prob_best = best_model.predict_proba(X_test)[:, 1]
auc_best = roc_auc_score(y_test, y_prob_best)

print(f"\nBest Params: {grid.best_params_}")
print(f"Tuned XGBoost AUC: {auc_best:.4f}")

importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': xgb.feature_importances_
}).sort_values(by='Importance', ascending=False)

print(f"\nTop 10 Features:\n{importance.head(10).to_string(index=False)}")

plt.figure(figsize=(10, 7))
plt.barh(importance['Feature'].head(15)[::-1], importance['Importance'].head(15)[::-1], color='steelblue', edgecolor='black')
plt.title('XGBoost Feature Importance (Top 15)')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('model_plots/xgb_feature_importance.png')
plt.close()

importance_lgbm = pd.DataFrame({
    'Feature': X.columns,
    'Importance': lgbm.feature_importances_
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 7))
plt.barh(importance_lgbm['Feature'].head(15)[::-1], importance_lgbm['Importance'].head(15)[::-1], color='darkorange', edgecolor='black')
plt.title('LightGBM Feature Importance (Top 15)')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('model_plots/lgbm_feature_importance.png')
plt.close()

plt.figure(figsize=(10, 6))
for y_prob, label, color in [
    (y_prob_lr,   f'Logistic Regression (AUC={auc_lr:.4f})',  'blue'),
    (y_prob_xgb,  f'XGBoost (AUC={auc_xgb:.4f})',            'green'),
    (y_prob_lgbm, f'LightGBM (AUC={auc_lgbm:.4f})',          'red'),
    (y_prob_best, f'Tuned XGBoost (AUC={auc_best:.4f})',      'purple'),
]:
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.plot(fpr, tpr, label=label, lw=2)

plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
plt.title('ROC Curve Comparison — All Models')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('model_plots/roc_comparison.png')
plt.close()

models = ['Logistic Regression', 'XGBoost', 'LightGBM', 'Tuned XGBoost']
aucs   = [auc_lr, auc_xgb, auc_lgbm, auc_best]
colors = ['#3498DB', '#2ECC71', '#E74C3C', '#9B59B6']

plt.figure(figsize=(10, 5))
bars = plt.bar(models, aucs, color=colors, edgecolor='black', width=0.5)
plt.ylim(0.5, 1.0)
plt.title('AUC-ROC Comparison Across All Models')
plt.ylabel('AUC-ROC Score')
for bar, auc in zip(bars, aucs):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
             f'{auc:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('model_plots/auc_comparison_bar.png')
plt.close()

y_pred_xgb  = xgb.predict(X_test)
y_pred_lgbm = lgbm.predict(X_test)

print("\n--- XGBoost Classification Report ---")
print(classification_report(y_test, y_pred_xgb, target_names=['No Default', 'Default']))

print("--- LightGBM Classification Report ---")
print(classification_report(y_test, y_pred_lgbm, target_names=['No Default', 'Default']))

for model_name, y_pred, y_prob in [
    ('XGBoost',  y_pred_xgb,  y_prob_xgb),
    ('LightGBM', y_pred_lgbm, y_prob_lgbm)
]:
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['No Default', 'Default'])
    fig, ax = plt.subplots(figsize=(7, 5))
    disp.plot(ax=ax, cmap='Blues', colorbar=False)
    plt.title(f'Confusion Matrix — {model_name}')
    plt.tight_layout()
    plt.savefig(f'model_plots/confusion_{model_name.lower()}.png')
    plt.close()

report = f"""
========================================
CreditPathAI - Milestone 4 Report
Student: Akhil Babu Gujjaralapudi
Models: XGBoost | LightGBM
========================================

AUC-ROC COMPARISON
-------------------
Logistic Regression : {auc_lr:.4f}
XGBoost (default)   : {auc_xgb:.4f}
LightGBM (default)  : {auc_lgbm:.4f}
Tuned XGBoost       : {auc_best:.4f}

BEST HYPERPARAMETERS (XGBoost GridSearch)
------------------------------------------
{grid.best_params_}

TOP 10 FEATURES (XGBoost)
--------------------------
{importance.head(10).to_string(index=False)}

TOP 10 FEATURES (LightGBM)
----------------------------
{importance_lgbm.head(10).to_string(index=False)}

MODEL PARAMETERS
-----------------
XGBoost  : n_estimators=100, max_depth=5, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8
LightGBM : n_estimators=100, max_depth=5, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8

PLOTS GENERATED (model_plots/)
--------------------------------
- xgb_feature_importance.png
- lgbm_feature_importance.png
- roc_comparison.png
- auc_comparison_bar.png
- confusion_xgboost.png
- confusion_lightgbm.png

NEXT STEPS (Milestone 5)
--------------------------
- Build Recommendation Engine
- Deploy with FastAPI
- Containerize with Docker
"""

with open('milestone4_report.txt', 'w') as f:
    f.write(report)

print(report)
print("=" * 60)
print("MILESTONE 4 COMPLETE!")
print("=" * 60)
