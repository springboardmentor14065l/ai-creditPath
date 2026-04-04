import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

# ----------- CREATE IMAGES FOLDER (IMPORTANT) -----------
os.makedirs("images", exist_ok=True)

# ----------- LOAD DATA -----------
df = pd.read_csv("data/final_features.csv")

print("Dataset Shape:", df.shape)

# ----------- SPLIT DATA -----------
X = df.drop("default_status", axis=1)
y = df["default_status"]

# ----------- CLEAN DATA -----------
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(X.median())

# ----------- TRAIN TEST SPLIT -----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----------- BASELINE -----------
auc_logistic = 0.72  # your value

# ----------- XGBOOST MODEL -----------
xgb = XGBClassifier(
    n_estimators=300,
    max_depth=3,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

xgb.fit(X_train, y_train)

# ----------- LIGHTGBM MODEL -----------
lgbm = LGBMClassifier(
    n_estimators=300,
    learning_rate=0.05,
    random_state=42
)

lgbm.fit(X_train, y_train)

# ----------- PREDICTIONS -----------
y_prob_xgb = xgb.predict_proba(X_test)[:, 1]
y_prob_lgbm = lgbm.predict_proba(X_test)[:, 1]

# ----------- AUC SCORES -----------
auc_xgb = roc_auc_score(y_test, y_prob_xgb)
auc_lgbm = roc_auc_score(y_test, y_prob_lgbm)

print("\n=== MODEL PERFORMANCE ===")
print("Baseline AUC:", auc_logistic)
print("XGBoost AUC:", round(auc_xgb, 4))
print("LightGBM AUC:", round(auc_lgbm, 4))

# ----------- BEST MODEL -----------
best_prob = y_prob_xgb if auc_xgb > auc_lgbm else y_prob_lgbm
best_auc = max(auc_xgb, auc_lgbm)

print("\n=== FINAL RESULT ===")
print("Best Model AUC:", round(best_auc, 4))

# ----------- MODEL COMPARISON GRAPH (SAVE) -----------
models = ["Baseline", "XGBoost", "LightGBM"]
scores = [auc_logistic, auc_xgb, auc_lgbm]

plt.figure()
plt.bar(models, scores)
plt.title("Model Comparison")
plt.ylabel("AUC Score")

plt.savefig("images/model_comparison.png")  # SAVE IMAGE
plt.close()

# ----------- ROC CURVE (SAVE) -----------
fpr, tpr, _ = roc_curve(y_test, best_prob)

plt.figure()
plt.plot(fpr, tpr, label="Best Model")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.savefig("images/roc_curve.png")  # SAVE IMAGE
plt.close()

print("\n✅ Graphs saved successfully in 'images/' folder!")