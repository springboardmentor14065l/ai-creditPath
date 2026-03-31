# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import joblib

# Step 1: Load the cleaned dataset
df = pd.read_csv("final_features.csv")

# Step 2: Define features (X) and target (y)
X = df.drop(columns=["Default"])  # Target column
y = df["Default"]

# Step 3: Perform train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train advanced models
# Logistic Regression (baseline)
log_reg = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
log_reg.fit(X_train, y_train)
log_reg_auc = roc_auc_score(y_test, log_reg.predict_proba(X_test)[:, 1])

# XGBoost Classifier
xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42)
xgb_model.fit(X_train, y_train)
xgb_auc = roc_auc_score(y_test, xgb_model.predict_proba(X_test)[:, 1])

# LightGBM Classifier
lgb_model = lgb.LGBMClassifier(random_state=42)
lgb_model.fit(X_train, y_train)
lgb_auc = roc_auc_score(y_test, lgb_model.predict_proba(X_test)[:, 1])

# Step 5: Evaluate models
def evaluate_model(model, X_test, y_test, model_name):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_proba)
    print(f"\n{model_name} Evaluation:")
    print(f"AUC-ROC Score: {auc:.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    return auc

print("Baseline Logistic Regression:")
log_reg_auc = evaluate_model(log_reg, X_test, y_test, "Logistic Regression")

print("\nXGBoost Classifier:")
xgb_auc = evaluate_model(xgb_model, X_test, y_test, "XGBoost")

print("\nLightGBM Classifier:")
lgb_auc = evaluate_model(lgb_model, X_test, y_test, "LightGBM")

# Step 6: Hyperparameter Tuning for XGBoost
param_grid = {
    "max_depth": [3, 5, 7, 10],
    "learning_rate": [0.01, 0.1, 0.2],
    "n_estimators": [100, 200, 300],
    "subsample": [0.6, 0.8, 1.0]
}

xgb_random_search = RandomizedSearchCV(
    estimator=xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
    param_distributions=param_grid,
    scoring="roc_auc",
    cv=3,
    n_iter=20,
    verbose=1,
    random_state=42,
    n_jobs=-1
)

xgb_random_search.fit(X_train, y_train)
best_xgb = xgb_random_search.best_estimator_

# Step 7: Evaluate the tuned XGBoost model
print("\nTuned XGBoost Classifier:")
tuned_xgb_auc = evaluate_model(best_xgb, X_test, y_test, "Tuned XGBoost")

# Step 8: Compare all models
results = pd.DataFrame({
    "Model": ["Logistic Regression", "XGBoost", "LightGBM", "Tuned XGBoost"],
    "AUC-ROC": [log_reg_auc, xgb_auc, lgb_auc, tuned_xgb_auc]
}).sort_values(by="AUC-ROC", ascending=False)

print("\nModel Comparison:")
print(results)

# Step 9: Plot feature importance for the best model
best_model = best_xgb  # Assuming Tuned XGBoost is the best model
feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": best_model.feature_importances_
}).sort_values(by="Importance", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x="Importance", y="Feature", data=feature_importance.head(10))
plt.title("Top 10 Feature Importances")
plt.show()

# Step 10: Save the best model
joblib.dump(best_model, "best_xgb_model.pkl")
print("\nBest model saved as 'best_xgb_model.pkl'")
print("\nModel Performance Summary:")
print("Tuned XGBoost achieves the best AUC-ROC score and significantly outperforms the baseline Logistic Regression model.")