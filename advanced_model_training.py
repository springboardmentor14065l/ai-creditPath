import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import xgboost as xgb
import lightgbm as lgb

# 1. Load dataset
print("Loading data...")
df = pd.read_csv("final_features.csv")

# 7. Simple Feature Engineering to improve performance
print("Adding simple features...")
df['interest_rate_score_interaction'] = df['interest_rate'] * (1000 - df['credit_score'])
df['monthly_interest_burden'] = df['interest_burden'] / df['loan_term']

# 2. Split data
X = df.drop('default_status', axis=1)
y = df['default_status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Calculate class weight for imbalance
ratio = float(y.value_counts()[0] / y.value_counts()[1])
print(f"Class ratio (unbalanced): {ratio:.2f}")

# 3. Train models with tuned parameters
print("\nTraining Advanced XGBoost...")
xgb_model = xgb.XGBClassifier(
    n_estimators=1000,
    learning_rate=0.03,
    max_depth=7,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=ratio,
    eval_metric='auc',
    early_stopping_rounds=50,
    random_state=42
)
xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

print("Training Advanced LightGBM...")
lgb_model = lgb.LGBMClassifier(
    n_estimators=1000,
    learning_rate=0.03,
    num_leaves=63,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=ratio,
    random_state=42,
    verbose=-1
)
lgb_model.fit(X_train, y_train)

# 4. Make predictions
xgb_probs = xgb_model.predict_proba(X_test)[:, 1]
lgb_probs = lgb_model.predict_proba(X_test)[:, 1]

# 5. Evaluate models
xgb_auc = roc_auc_score(y_test, xgb_probs)
lgb_auc = roc_auc_score(y_test, lgb_probs)

# 6. Compare performance
print("\n===== AUC COMPARISON (IMPROVED) =====")
print(f"XGBoost AUC: {xgb_auc:.4f}")
print(f"LightGBM AUC: {lgb_auc:.4f}")

# 8. Extract feature importance from XGBoost
print("\nTop 5 Important Features (XGBoost):")
importances = xgb_model.feature_importances_
feature_names = X.columns
feat_importances = pd.Series(importances, index=feature_names)
print(feat_importances.nlargest(5))

# Save final model results
pd.DataFrame({
    'Model': ['XGBoost', 'LightGBM'],
    'AUC': [xgb_auc, lgb_auc]
}).to_csv("advanced_model_results.csv", index=False)
