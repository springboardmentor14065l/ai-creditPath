import os
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

print("=" * 60)
print("  CREDITPATH AI — ADVANCED MODEL TRAINING (FIXED)")
print("=" * 60)

print("\n[1/6] Loading data and cleaning features...")
df = pd.read_csv(os.path.join(DATA_DIR, "final_features.csv"))
df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True)
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(df.median(numeric_only=True), inplace=True)

X = df.drop("Status", axis=1)
y = df["Status"]
print(f"  → Shape: {X.shape}, Default rate: {y.mean():.2%}")

# NOTE: We do NOT drop correlated features — they ARE legitimate risk signals.
# NOTE: We do NOT add noise — it hinders the model's ability to learn real patterns.

print("\n[2/6] Splitting data (80/20 stratified)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"  → Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")

print("\n[3/6] Training XGBoost (GridSearchCV)...")
param_grid_xgb = {
    "max_depth": [4, 6],
    "learning_rate": [0.05, 0.1],
    "n_estimators": [100, 200]
}
grid_xgb = GridSearchCV(
    XGBClassifier(
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=1.0,
        reg_lambda=2.0,
        min_child_weight=10,
        gamma=0.1,
        random_state=42,
        eval_metric="logloss",
        use_label_encoder=False
    ),
    param_grid_xgb,
    scoring="roc_auc",
    cv=3,
    n_jobs=-1
)
grid_xgb.fit(X_train, y_train)
xgb_tuned = grid_xgb.best_estimator_
y_prob_xgb = xgb_tuned.predict_proba(X_test)[:, 1]
auc_xgb = roc_auc_score(y_test, y_prob_xgb)
print(f"  → Best params: {grid_xgb.best_params_}")
print(f"  → AUC-ROC: {auc_xgb:.4f}")

print("\n[4/6] Training LightGBM (GridSearchCV)...")
param_grid_lgbm = {
    "max_depth": [4, 6],
    "learning_rate": [0.05, 0.1],
    "n_estimators": [100, 200]
}
grid_lgbm = GridSearchCV(
    LGBMClassifier(
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=1.0,
        reg_lambda=2.0,
        min_child_weight=10,
        random_state=42,
        verbose=-1
    ),
    param_grid_lgbm,
    scoring="roc_auc",
    cv=3,
    n_jobs=-1
)
grid_lgbm.fit(X_train, y_train)
lgbm_tuned = grid_lgbm.best_estimator_
y_prob_lgbm = lgbm_tuned.predict_proba(X_test)[:, 1]
auc_lgbm = roc_auc_score(y_test, y_prob_lgbm)
print(f"  → Best params: {grid_lgbm.best_params_}")
print(f"  → AUC-ROC: {auc_lgbm:.4f}")

print("\n[5/6] Training Stacked Ensemble (OOF Meta-Learner)...")
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

oof_xgb = cross_val_predict(
    XGBClassifier(**grid_xgb.best_params_, subsample=0.8, colsample_bytree=0.8,
                  reg_alpha=1.0, reg_lambda=2.0, min_child_weight=10, gamma=0.1,
                  random_state=42, eval_metric="logloss"),
    X_train, y_train, cv=skf, method="predict_proba"
)[:, 1]

oof_lgbm = cross_val_predict(
    LGBMClassifier(**grid_lgbm.best_params_, subsample=0.8, colsample_bytree=0.8,
                   reg_alpha=1.0, reg_lambda=2.0, min_child_weight=10,
                   random_state=42, verbose=-1),
    X_train, y_train, cv=skf, method="predict_proba"
)[:, 1]

meta_train = np.column_stack([oof_xgb, oof_lgbm])
meta_test = np.column_stack([xgb_tuned.predict_proba(X_test)[:, 1],
                              lgbm_tuned.predict_proba(X_test)[:, 1]])

meta_learner = LogisticRegression(random_state=42, max_iter=1000).fit(meta_train, y_train)
y_prob_ensemble = meta_learner.predict_proba(meta_test)[:, 1]
auc_ensemble = roc_auc_score(y_test, y_prob_ensemble)
print(f"  → Ensemble AUC-ROC: {auc_ensemble:.4f}")
print(f"  → Probability range: [{y_prob_ensemble.min():.4f}, {y_prob_ensemble.max():.4f}]")

# Risk segmentation check
risk_df = pd.DataFrame({"actual": y_test.values, "probability": y_prob_ensemble})
risk_df["risk_segment"] = pd.cut(
    risk_df["probability"],
    bins=[0, 0.3, 0.6, 1.0],
    labels=["Low Risk", "Medium Risk", "High Risk"]
)
seg = risk_df.groupby("risk_segment", observed=False).agg(
    count=("actual", "size"),
    actual_default_rate=("actual", "mean"),
    avg_predicted_prob=("probability", "mean")
).round(4)
print(f"\n  Risk Segmentation:\n{seg.to_string()}")
seg.to_csv(os.path.join(OUTPUT_DIR, "risk_segmentation.csv"))

print("\n[6/6] Saving models and feature importance...")
joblib.dump(xgb_tuned, os.path.join(OUTPUT_DIR, "xgb_tuned_model.pkl"))
joblib.dump(lgbm_tuned, os.path.join(OUTPUT_DIR, "lgbm_tuned_model.pkl"))
joblib.dump(meta_learner, os.path.join(OUTPUT_DIR, "stacked_ensemble_meta.pkl"))
print("  → xgb_tuned_model.pkl saved ✅")
print("  → lgbm_tuned_model.pkl saved ✅")
print("  → stacked_ensemble_meta.pkl saved ✅")

# Feature importance CSV
xgb_imp = dict(zip(X.columns, xgb_tuned.feature_importances_))
lgbm_imp = dict(zip(X.columns, lgbm_tuned.feature_importances_))
imp_df = pd.DataFrame({
    "Feature": list(X.columns),
    "XGBoost_Importance": [xgb_imp.get(f, 0) for f in X.columns],
    "LightGBM_Importance": [lgbm_imp.get(f, 0) for f in X.columns],
})
imp_df["Avg_Importance"] = (imp_df["XGBoost_Importance"] + imp_df["LightGBM_Importance"]) / 2
imp_df = imp_df.sort_values("Avg_Importance", ascending=False)
imp_df.to_csv(os.path.join(OUTPUT_DIR, "advanced_feature_importance.csv"), index=False)
print("  → advanced_feature_importance.csv saved ✅")

print("\n" + "=" * 60)
print("  FINAL AUC-ROC RESULTS")
print("=" * 60)
print(f"  {'Stacked Ensemble':<30} {auc_ensemble:.4f}")
print(f"  {'LightGBM (Tuned)':<30} {auc_lgbm:.4f}")
print(f"  {'XGBoost (Tuned)':<30} {auc_xgb:.4f}")
print("=" * 60)

print("\n  Tuned XGBoost Classification Report:")
print(classification_report(y_test, xgb_tuned.predict(X_test), target_names=["Non-Default", "Default"]))
print("\n  Stacked Ensemble Classification Report:")
print(classification_report(y_test, meta_learner.predict(meta_test), target_names=["Non-Default", "Default"]))
print("=" * 60)
print("  ✅ Training complete!")