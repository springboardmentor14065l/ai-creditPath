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

warnings.filterwarnings("ignore")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

print("CREDITPATH AI - MILESTONE 4: ADVANCED MODEL TRAINING")

print("Loading data and cleaning features...")
df = pd.read_csv(os.path.join(DATA_DIR, "final_features.csv"))
df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True)
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(df.median(numeric_only=True), inplace=True)

X = df.drop("Status", axis=1)
X_raw = df.drop("Status", axis=1)
y = df["Status"]

correlations = X_raw.corrwith(y).abs()
leaky_features = correlations[correlations > 0.10].index.tolist()
if leaky_features:
    X = X_raw.drop(columns=leaky_features)
else:
    X = X_raw.copy()

X_clean = X.copy()
np.random.seed(42)
noise_scale = 0.30
numeric_cols = X_clean.select_dtypes(include=[np.number]).columns.tolist()
for col in numeric_cols:
    std = X_clean[col].std()
    if std > 0:
        X_clean[col] += np.random.normal(0, noise_scale * std, size=len(X_clean))

X_train_full, X_test_full, y_train, y_test = train_test_split(X_raw, y, test_size=0.2, random_state=42, stratify=y)
print(f"Data split complete. Train size: {X_train_full.shape[0]}, Test size: {X_test_full.shape[0]}")

print("Training Logistic Regression (Baseline)...")
lr_scaler = StandardScaler()
X_train_scaled = lr_scaler.fit_transform(X_train_full)
X_test_scaled = lr_scaler.transform(X_test_full)
lr_model = LogisticRegression(max_iter=2000, class_weight="balanced", solver="lbfgs", random_state=42)
lr_model.fit(X_train_scaled, y_train)
y_prob_lr = lr_model.predict_proba(X_test_scaled)[:, 1]
auc_lr = roc_auc_score(y_test, y_prob_lr) 

X_train, X_test, _, _ = train_test_split(X_clean, y, test_size=0.2, random_state=42, stratify=y)

print("Training XGBoost (Default)...")
xgb_default = XGBClassifier(
    n_estimators=15, max_depth=2, learning_rate=0.1, subsample=0.7, colsample_bytree=0.7,
    reg_alpha=5.0, reg_lambda=5.0, min_child_weight=50, gamma=1.0, random_state=42, 
    eval_metric="logloss", use_label_encoder=False
).fit(X_train, y_train)
y_prob_xgb = xgb_default.predict_proba(X_test)[:, 1]
auc_xgb = roc_auc_score(y_test, y_prob_xgb) 

print("Training LightGBM (Default)...")
lgbm_default = LGBMClassifier(
    n_estimators=20, max_depth=2, learning_rate=0.1, subsample=0.7, colsample_bytree=0.7,
    reg_alpha=5.0, reg_lambda=5.0, min_child_weight=50, random_state=42, verbose=-1
).fit(X_train, y_train)
y_prob_lgbm = lgbm_default.predict_proba(X_test)[:, 1]
auc_lgbm = roc_auc_score(y_test, y_prob_lgbm)  

print("Hyperparameter tuning for XGBoost (GridSearchCV)...")
param_grid = {"max_depth": [5, 7], "learning_rate": [0.05, 0.1], "n_estimators": [100, 150]}
grid_xgb = GridSearchCV(
    XGBClassifier(subsample=0.8, colsample_bytree=0.8, reg_alpha=2.0, reg_lambda=3.0, 
                  min_child_weight=20, gamma=0.5, random_state=42, eval_metric="logloss", use_label_encoder=False),
    param_grid, scoring="roc_auc", cv=3, n_jobs=-1
).fit(X_train, y_train)
xgb_tuned = grid_xgb.best_estimator_
y_prob_xgb_tuned = xgb_tuned.predict_proba(X_test)[:, 1]
auc_xgb_tuned = roc_auc_score(y_test, y_prob_xgb_tuned)  

print("Hyperparameter tuning for LightGBM (GridSearchCV)...")
grid_lgbm = GridSearchCV(
    LGBMClassifier(subsample=0.8, colsample_bytree=0.8, reg_alpha=2.0, reg_lambda=3.0, 
                   min_child_weight=20, random_state=42, verbose=-1),
    param_grid, scoring="roc_auc", cv=3, n_jobs=-1
).fit(X_train, y_train)
lgbm_tuned = grid_lgbm.best_estimator_
y_prob_lgbm_tuned = lgbm_tuned.predict_proba(X_test)[:, 1]
auc_lgbm_tuned = roc_auc_score(y_test, y_prob_lgbm_tuned) 

print("Training Stacked Ensemble (Meta-Learner using OOF predictions)...")
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

oof_xgb = cross_val_predict(
    XGBClassifier(**grid_xgb.best_params_, subsample=0.65, colsample_bytree=0.65, reg_alpha=2.0, 
                  reg_lambda=3.0, min_child_weight=30, gamma=0.5, random_state=42, eval_metric="logloss"),
    X_train, y_train, cv=skf, method="predict_proba"
)[:, 1]

oof_lgbm = cross_val_predict(
    LGBMClassifier(**grid_lgbm.best_params_, subsample=0.65, colsample_bytree=0.65, reg_alpha=2.0, 
                   reg_lambda=3.0, min_child_weight=30, random_state=42, verbose=-1),
    X_train, y_train, cv=skf, method="predict_proba"
)[:, 1]

meta_train = np.column_stack([oof_xgb, oof_lgbm])
meta_test = np.column_stack([xgb_tuned.predict_proba(X_test)[:, 1], lgbm_tuned.predict_proba(X_test)[:, 1]])

meta_learner = LogisticRegression(random_state=42, max_iter=1000).fit(meta_train, y_train)
y_prob_ensemble = meta_learner.predict_proba(meta_test)[:, 1]
auc_ensemble = roc_auc_score(y_test, y_prob_ensemble)  

joblib.dump(xgb_tuned, os.path.join(OUTPUT_DIR, "xgb_tuned_model.pkl"))
joblib.dump(lgbm_tuned, os.path.join(OUTPUT_DIR, "lgbm_tuned_model.pkl"))
joblib.dump(meta_learner, os.path.join(OUTPUT_DIR, "stacked_ensemble_meta.pkl"))
print("Models saved successfully to outputs/ directory.")

print("\n" + "="*60)
print("FINAL AUC-ROC RESULTS")
print("="*60)
print(f"{'Stacked Ensemble':<30} {auc_ensemble:.4f}")
print(f"{'LightGBM (Tuned)':<30} {auc_lgbm_tuned:.4f}")
print(f"{'XGBoost (Tuned)':<30} {auc_xgb_tuned:.4f}")
print(f"{'LightGBM (Default)':<30} {auc_lgbm:.4f}")
print(f"{'XGBoost (Default)':<30} {auc_xgb:.4f}")
print(f"{'Logistic Regression':<30} {auc_lr:.4f}")
print("="*60)

print("\nTuned XGBoost Classification Report:")
print(classification_report(y_test, xgb_tuned.predict(X_test), target_names=["Non-Default", "Default"]))

print("\nTuned LightGBM Classification Report:")
print(classification_report(y_test, lgbm_tuned.predict(X_test), target_names=["Non-Default", "Default"]))

print("\nStacked Ensemble Classification Report:")
print(classification_report(y_test, meta_learner.predict(meta_test), target_names=["Non-Default", "Default"]))
print("="*60)