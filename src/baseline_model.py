
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    classification_report,
    precision_recall_curve,
    average_precision_score,
    f1_score,
    accuracy_score,
)
import joblib

warnings.filterwarnings("ignore")

# ────────────────────────────────────────────
# Output directory for plots and artifacts
# ────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ====================================================
# STEP 1: Load Dataset
# ====================================================
print("=" * 60)
print("  STEP 1: Loading Dataset")
print("=" * 60)

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", "final_features.csv"))

# Clean column names (remove special chars)
df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True)

# Handle inf values → replace with NaN, then fill with column median
inf_count = np.isinf(df.select_dtypes(include=[np.number]).values).sum()
if inf_count > 0:
    print(f"  ⚠️  Found {inf_count} inf values — replacing with median...")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(df.median(numeric_only=True), inplace=True)

print(f"  → Dataset shape : {df.shape}")
print(f"  → Target column : Status")
print(f"  → Class distribution:\n{df['Status'].value_counts()}")
print(f"  → Default rate   : {df['Status'].mean():.2%}")
print()

# ====================================================
# STEP 2: Define Features and Target
# ====================================================
print("=" * 60)
print("  STEP 2: Define Features and Target")
print("=" * 60)

X = df.drop("Status", axis=1)
y = df["Status"]

feature_names = list(X.columns)
print(f"  → Number of features: {len(feature_names)}")
print(f"  → Features: {feature_names[:10]}... (showing first 10)")
print()

# ====================================================
# STEP 3: Train-Test Split (80/20, stratified)
# ====================================================
print("=" * 60)
print("  STEP 3: Train-Test Split")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"  → Training set : {X_train.shape[0]} samples")
print(f"  → Testing set  : {X_test.shape[0]} samples")
print(f"  → Train default rate: {y_train.mean():.2%}")
print(f"  → Test default rate : {y_test.mean():.2%}")
print()

# ====================================================
# STEP 4: Scaling (MANDATORY — StandardScaler)
# ====================================================
print("=" * 60)
print("  STEP 4: Feature Scaling (StandardScaler)")
print("=" * 60)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("  → Scaling applied ✅")
print(f"  → Mean of scaled train (first 5): {X_train_scaled.mean(axis=0)[:5].round(6)}")
print(f"  → Std of scaled train  (first 5): {X_train_scaled.std(axis=0)[:5].round(6)}")
print()

# ====================================================
# STEP 5: Train Model (Logistic Regression)
# ====================================================
print("=" * 60)
print("  STEP 5: Training Logistic Regression")
print("=" * 60)

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",   # handles class imbalance
    solver="lbfgs",
    random_state=42
)
model.fit(X_train_scaled, y_train)

print("  → Model trained ✅")
print(f"  → Solver: lbfgs | Max iter: 2000 | class_weight: balanced")
print()

# ====================================================
# STEP 6: Predictions
# ====================================================
print("=" * 60)
print("  STEP 6: Predictions")
print("=" * 60)

y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]

print(f"  → Predicted positives: {y_pred.sum()} / {len(y_pred)}")
print(f"  → Probability range  : [{y_prob.min():.4f}, {y_prob.max():.4f}]")
print()

# ====================================================
# STEP 7: Evaluation — AUC-ROC + Full Metrics
# ====================================================
print("=" * 60)
print("  STEP 7: Evaluation")
print("=" * 60)

auc = roc_auc_score(y_test, y_prob)
f1  = f1_score(y_test, y_pred)
acc = accuracy_score(y_test, y_pred)
ap  = average_precision_score(y_test, y_prob)

# AUC rating
if auc >= 0.80:
    auc_label = "🌟 EXCELLENT"
elif auc >= 0.75:
    auc_label = "✅ VERY GOOD"
elif auc >= 0.70:
    auc_label = "👍 GOOD"
elif auc >= 0.65:
    auc_label = "⚠️  FAIR — consider improving features"
else:
    auc_label = "❌ POOR — revisit feature engineering"

print(f"  ┌──────────────────────────────────────────┐")
print(f"  │  AUC-ROC          : {auc:.4f}  {auc_label}")
print(f"  │  F1 Score         : {f1:.4f}")
print(f"  │  Accuracy         : {acc:.4f}")
print(f"  │  Avg Precision    : {ap:.4f}")
print(f"  └──────────────────────────────────────────┘")
print()

# Classification Report
print("  📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Non-Default", "Default"]))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("  📊 Confusion Matrix:")
print(f"     TN={cm[0,0]:>6}   FP={cm[0,1]:>6}")
print(f"     FN={cm[1,0]:>6}   TP={cm[1,1]:>6}")
print()

# ====================================================
# 🔥 UNIQUE #1 — Stratified K-Fold Cross-Validation
# ====================================================
print("=" * 60)
print("  🔥 UNIQUE: Stratified 5-Fold Cross-Validation")
print("=" * 60)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(
    LogisticRegression(max_iter=2000, class_weight="balanced", solver="lbfgs", random_state=42),
    scaler.fit_transform(X), y,
    cv=cv,
    scoring="roc_auc"
)

print(f"  → Fold AUCs     : {np.round(cv_scores, 4)}")
print(f"  → Mean AUC      : {cv_scores.mean():.4f}")
print(f"  → Std AUC       : {cv_scores.std():.4f}")
print(f"  → 95% CI        : [{cv_scores.mean() - 1.96*cv_scores.std():.4f}, "
      f"{cv_scores.mean() + 1.96*cv_scores.std():.4f}]")
print()

# ====================================================
# STEP 8: Coefficient Interpretation
# ====================================================
print("=" * 60)
print("  STEP 8: Feature Coefficient Interpretation")
print("=" * 60)

coeff_df = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": model.coef_[0],
    "Abs_Coefficient": np.abs(model.coef_[0])
}).sort_values(by="Abs_Coefficient", ascending=False)

print("\n  🔺 TOP 10 Features INCREASING Default Risk (positive coeff):")
top_positive = coeff_df[coeff_df["Coefficient"] > 0].head(10)
for _, row in top_positive.iterrows():
    print(f"    + {row['Feature']:<35} coeff = {row['Coefficient']:>+.4f}")

print("\n  🔻 TOP 10 Features DECREASING Default Risk (negative coeff):")
top_negative = coeff_df[coeff_df["Coefficient"] < 0].sort_values("Coefficient").head(10)
for _, row in top_negative.iterrows():
    print(f"    - {row['Feature']:<35} coeff = {row['Coefficient']:>+.4f}")

# Save full coefficient table
coeff_df.to_csv(os.path.join(OUTPUT_DIR, "feature_coefficients.csv"), index=False)
print(f"\n  → Full coefficient table saved to outputs/feature_coefficients.csv")
print()

# ====================================================
# 🔥 UNIQUE #2 — Risk Segmentation
# ====================================================
print("=" * 60)
print("  🔥 UNIQUE: Borrower Risk Segmentation")
print("=" * 60)

risk_df = pd.DataFrame({
    "actual": y_test.values,
    "probability": y_prob
})

risk_df["risk_segment"] = pd.cut(
    risk_df["probability"],
    bins=[0, 0.3, 0.6, 1.0],
    labels=["🟢 Low Risk", "🟡 Medium Risk", "🔴 High Risk"]
)

segment_summary = risk_df.groupby("risk_segment", observed=False).agg(
    count=("actual", "size"),
    actual_default_rate=("actual", "mean"),
    avg_predicted_prob=("probability", "mean")
).round(4)

print(segment_summary.to_string())
segment_summary.to_csv(os.path.join(OUTPUT_DIR, "risk_segmentation.csv"))
print(f"\n  → Risk segmentation saved to outputs/risk_segmentation.csv")
print()

# ====================================================
# VISUALIZATION 1: ROC Curve
# ====================================================
print("=" * 60)
print("  📈 Generating ROC Curve Plot...")
print("=" * 60)

fpr, tpr, _ = roc_curve(y_test, y_prob)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(fpr, tpr, color="#2563EB", lw=2.5, label=f"Logistic Regression (AUC = {auc:.4f})")
ax.plot([0, 1], [0, 1], color="#94A3B8", linestyle="--", lw=1.5, label="Random Classifier")
ax.fill_between(fpr, tpr, alpha=0.15, color="#2563EB")
ax.set_xlabel("False Positive Rate", fontsize=12)
ax.set_ylabel("True Positive Rate", fontsize=12)
ax.set_title("CreditPathAI — ROC Curve (Baseline Logistic Regression)", fontsize=14, fontweight="bold")
ax.legend(loc="lower right", fontsize=11)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "roc_curve.png"), dpi=150)
plt.close(fig)
print("  → Saved to outputs/roc_curve.png ✅")
print()

# ====================================================
# VISUALIZATION 2: Confusion Matrix Heatmap
# ====================================================
print("  📈 Generating Confusion Matrix Heatmap...")

fig, ax = plt.subplots(figsize=(7, 5.5))
sns.heatmap(
    cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=["Non-Default", "Default"],
    yticklabels=["Non-Default", "Default"],
    ax=ax, annot_kws={"size": 16}
)
ax.set_xlabel("Predicted", fontsize=12)
ax.set_ylabel("Actual", fontsize=12)
ax.set_title("Confusion Matrix — Logistic Regression Baseline", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "confusion_matrix.png"), dpi=150)
plt.close(fig)
print("  → Saved to outputs/confusion_matrix.png ✅")
print()

# ====================================================
# VISUALIZATION 3: Top Feature Importances
# ====================================================
print("  📈 Generating Feature Importance Chart...")

top20 = coeff_df.head(20).copy()
top20 = top20.sort_values("Abs_Coefficient", ascending=True)

colors = ["#EF4444" if c > 0 else "#22C55E" for c in top20["Coefficient"]]

fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(top20["Feature"], top20["Coefficient"], color=colors, edgecolor="#1E293B", linewidth=0.5)
ax.set_xlabel("Coefficient Value", fontsize=12)
ax.set_title("Top 20 Most Important Features (Logistic Regression)", fontsize=14, fontweight="bold")
ax.axvline(x=0, color="#1E293B", linewidth=0.8)

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#EF4444", label="Increases Default Risk"),
    Patch(facecolor="#22C55E", label="Decreases Default Risk"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=10)
ax.grid(True, axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "feature_importance.png"), dpi=150)
plt.close(fig)
print("  → Saved to outputs/feature_importance.png ✅")
print()

# ====================================================
# VISUALIZATION 4: Precision-Recall Curve  🔥 UNIQUE
# ====================================================
print("  📈 Generating Precision-Recall Curve...")

precision, recall, _ = precision_recall_curve(y_test, y_prob)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(recall, precision, color="#8B5CF6", lw=2.5, label=f"Avg Precision = {ap:.4f}")
ax.fill_between(recall, precision, alpha=0.15, color="#8B5CF6")
ax.set_xlabel("Recall", fontsize=12)
ax.set_ylabel("Precision", fontsize=12)
ax.set_title("Precision-Recall Curve — Logistic Regression Baseline", fontsize=14, fontweight="bold")
ax.legend(loc="upper right", fontsize=11)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "precision_recall_curve.png"), dpi=150)
plt.close(fig)
print("  → Saved to outputs/precision_recall_curve.png ✅")
print()

# ====================================================
# VISUALIZATION 5: Risk Segment Distribution  🔥 UNIQUE
# ====================================================
print("  📈 Generating Risk Segmentation Chart...")

seg_counts = risk_df["risk_segment"].value_counts().reindex(
    ["🟢 Low Risk", "🟡 Medium Risk", "🔴 High Risk"]
)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(
    ["Low Risk", "Medium Risk", "High Risk"],
    seg_counts.values,
    color=["#22C55E", "#F59E0B", "#EF4444"],
    edgecolor="#1E293B",
    linewidth=0.8,
    width=0.6
)

for bar, count in zip(bars, seg_counts.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
        f"{count:,}", ha='center', va='bottom', fontweight='bold', fontsize=12
    )

ax.set_ylabel("Number of Borrowers", fontsize=12)
ax.set_title("Borrower Risk Segmentation Distribution", fontsize=14, fontweight="bold")
ax.grid(True, axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "risk_segmentation.png"), dpi=150)
plt.close(fig)
print("  → Saved to outputs/risk_segmentation.png ✅")
print()

# ====================================================
# 🔥 UNIQUE #3 — Save Model & Scaler (Production Ready)
# ====================================================
print("=" * 60)
print("  🔥 UNIQUE: Saving Model & Scaler Artifacts")
print("=" * 60)

joblib.dump(model, os.path.join(OUTPUT_DIR, "logistic_model.pkl"))
joblib.dump(scaler, os.path.join(OUTPUT_DIR, "scaler.pkl"))
print("  → Model saved  : outputs/logistic_model.pkl ✅")
print("  → Scaler saved  : outputs/scaler.pkl ✅")
print()

# ====================================================
# FINAL SUMMARY
# ====================================================
print("═" * 60)
print("  ✅ MILESTONE 3 COMPLETE — SUMMARY")
print("═" * 60)
print(f"  │ AUC-ROC (test)           : {auc:.4f}  {auc_label}")
print(f"  │ AUC-ROC (5-fold CV mean) : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print(f"  │ F1 Score                 : {f1:.4f}")
print(f"  │ Accuracy                 : {acc:.4f}")
print(f"  │ Average Precision        : {ap:.4f}")
print(f"  │ Top Risk Factor          : {coeff_df.iloc[0]['Feature']}")
print(f"  │")
print(f"  │ Artifacts Generated:")
print(f"  │   → outputs/roc_curve.png")
print(f"  │   → outputs/confusion_matrix.png")
print(f"  │   → outputs/feature_importance.png")
print(f"  │   → outputs/precision_recall_curve.png")
print(f"  │   → outputs/risk_segmentation.png")
print(f"  │   → outputs/risk_segmentation.csv")
print(f"  │   → outputs/feature_coefficients.csv")
print(f"  │   → outputs/logistic_model.pkl")
print(f"  │   → outputs/scaler.pkl")
print("═" * 60)
