import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve

# Load dataset :contentReference[oaicite:0]{index=0}
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "final_features.csv"))
df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True)

# Handle inf / NaN
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(df.median(numeric_only=True), inplace=True)

# Features / Target
X = df.drop("Status", axis=1)
y = df["Status"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model
model = LogisticRegression(max_iter=2000, class_weight="balanced")
model.fit(X_train, y_train)

# Predictions
y_prob = model.predict_proba(X_test)[:, 1]

# AUC score
auc = roc_auc_score(y_test, y_prob)
print(f"\nAUC-ROC (Test): {auc:.4f}")

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)

plt.figure(figsize=(7,5))
plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}")
plt.plot([0,1], [0,1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.grid()
plt.savefig("roc_curve.png")
plt.close()

# Cross-validation AUC
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(
    LogisticRegression(max_iter=2000, class_weight="balanced"),
    scaler.fit_transform(X), y,
    cv=cv, scoring="roc_auc"
)

print(f"CV AUC Scores : {np.round(cv_scores, 4)}")
print(f"Mean AUC      : {cv_scores.mean():.4f}")
print(f"Std AUC       : {cv_scores.std():.4f}")