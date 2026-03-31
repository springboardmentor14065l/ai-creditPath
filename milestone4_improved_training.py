# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report, roc_curve, auc, precision_recall_curve, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

print("=" * 80)
print("MILESTONE 4: ADVANCED MODEL TRAINING WITH CLASS IMBALANCE HANDLING")
print("=" * 80)

# Step 1: Load the cleaned dataset
print("\nStep 1: Loading dataset...")
df = pd.read_csv("final_features.csv")
print(f"Dataset shape: {df.shape}")
print(f"Class distribution:\n{df['Default'].value_counts()}")
print(f"Class imbalance ratio: {df['Default'].value_counts()[0] / df['Default'].value_counts()[1]:.2f}:1")

# Step 2: Define features (X) and target (y)
print("\nStep 2: Preparing features and target...")
X = df.drop(columns=["Default"])
y = df["Default"]

# Step 3: Perform stratified train-test split (maintains class distribution)
print("\nStep 3: Performing stratified train-test split...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Training set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Step 4: Handle class imbalance with SMOTE
print("\nStep 4: Handling class imbalance with SMOTE...")
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
print(f"Balanced training set shape: {X_train_balanced.shape}")
print(f"Balanced class distribution:\n{pd.Series(y_train_balanced).value_counts()}")

# Step 5: Scale features for Logistic Regression
print("\nStep 5: Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_balanced)
X_test_scaled = scaler.transform(X_test)

# Step 6: Train baseline model with class weights
print("\nStep 6: Training baseline Logistic Regression model...")
log_reg = LogisticRegression(
    max_iter=1000, 
    class_weight="balanced", 
    random_state=42,
    solver='lbfgs'
)
log_reg.fit(X_train_scaled, y_train_balanced)
log_reg_pred_proba = log_reg.predict_proba(X_test_scaled)[:, 1]
log_reg_auc = roc_auc_score(y_test, log_reg_pred_proba)
print(f"Logistic Regression AUC-ROC: {log_reg_auc:.4f}")

# Step 7: Train initial XGBoost model
print("\nStep 7: Training initial XGBoost model...")
# Calculate scale_pos_weight for class imbalance
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
xgb_model = xgb.XGBClassifier(
    random_state=42,
    scale_pos_weight=scale_pos_weight,
    tree_method='hist',
    verbosity=0
)
xgb_model.fit(X_train, y_train)
xgb_pred_proba = xgb_model.predict_proba(X_test)[:, 1]
xgb_auc = roc_auc_score(y_test, xgb_pred_proba)
print(f"XGBoost AUC-ROC: {xgb_auc:.4f}")

# Step 8: Train initial LightGBM model
print("\nStep 8: Training initial LightGBM model...")
lgb_model = lgb.LGBMClassifier(
    random_state=42,
    is_unbalance=True,
    verbose=-1
)
lgb_model.fit(X_train, y_train)
lgb_pred_proba = lgb_model.predict_proba(X_test)[:, 1]
lgb_auc = roc_auc_score(y_test, lgb_pred_proba)
print(f"LightGBM AUC-ROC: {lgb_auc:.4f}")

# Step 9: Comprehensive model evaluation function
def evaluate_model_comprehensive(model, X_test, y_test, model_name):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_proba)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\n{model_name} Comprehensive Evaluation:")
    print(f"AUC-ROC Score: {auc:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    return auc, f1

print("\n" + "=" * 80)
print("INITIAL MODEL EVALUATION")
print("=" * 80)
log_auc, log_f1 = evaluate_model_comprehensive(log_reg, X_test_scaled, y_test, "Logistic Regression")
xgb_auc, xgb_f1 = evaluate_model_comprehensive(xgb_model, X_test, y_test, "XGBoost")
lgb_auc, lgb_f1 = evaluate_model_comprehensive(lgb_model, X_test, y_test, "LightGBM")

# Step 10: Advanced Hyperparameter Tuning for XGBoost
print("\n" + "=" * 80)
print("HYPERPARAMETER TUNING FOR XGBOOST")
print("=" * 80)

param_grid = {
    "max_depth": [4, 5, 6, 7, 8],
    "learning_rate": [0.01, 0.05, 0.1, 0.15],
    "n_estimators": [100, 200, 300],
    "subsample": [0.7, 0.8, 0.9, 1.0],
    "colsample_bytree": [0.7, 0.8, 0.9, 1.0],
    "gamma": [0, 0.1, 0.5],
    "min_child_weight": [1, 2, 3]
}

print(f"Tuning XGBoost with {len(param_grid)} parameters...")
xgb_random_search = RandomizedSearchCV(
    estimator=xgb.XGBClassifier(
        random_state=42,
        scale_pos_weight=scale_pos_weight,
        tree_method='hist',
        verbosity=0
    ),
    param_distributions=param_grid,
    scoring="roc_auc",
    cv=StratifiedKFold(n_splits=3, shuffle=True, random_state=42),
    n_iter=20,
    verbose=1,
    random_state=42,
    n_jobs=-1
)

xgb_random_search.fit(X_train, y_train)
best_xgb = xgb_random_search.best_estimator_
print(f"\nBest XGBoost parameters: {xgb_random_search.best_params_}")
print(f"Best cross-validation AUC-ROC: {xgb_random_search.best_score_:.4f}")

# Step 11: Advanced Hyperparameter Tuning for LightGBM
print("\n" + "=" * 80)
print("HYPERPARAMETER TUNING FOR LIGHTGBM")
print("=" * 80)

param_grid_lgb = {
    "num_leaves": [20, 30, 40],
    "learning_rate": [0.01, 0.05, 0.1],
    "n_estimators": [100, 200, 300],
    "subsample": [0.7, 0.8, 0.9, 1.0],
    "colsample_bytree": [0.7, 0.8, 0.9, 1.0],
    "reg_alpha": [0, 0.5],
    "reg_lambda": [0, 0.5]
}

print(f"Tuning LightGBM with {len(param_grid_lgb)} parameters...")
lgb_random_search = RandomizedSearchCV(
    estimator=lgb.LGBMClassifier(
        random_state=42,
        is_unbalance=True,
        verbose=-1,
        n_jobs=-1
    ),
    param_distributions=param_grid_lgb,
    scoring="roc_auc",
    cv=StratifiedKFold(n_splits=3, shuffle=True, random_state=42),
    n_iter=20,
    verbose=1,
    random_state=42,
    n_jobs=-1
)

lgb_random_search.fit(X_train, y_train)
best_lgb = lgb_random_search.best_estimator_
print(f"\nBest LightGBM parameters: {lgb_random_search.best_params_}")
print(f"Best cross-validation AUC-ROC: {lgb_random_search.best_score_:.4f}")

# Step 12: Evaluate tuned models
print("\n" + "=" * 80)
print("TUNED MODEL EVALUATION")
print("=" * 80)
tuned_xgb_auc, tuned_xgb_f1 = evaluate_model_comprehensive(best_xgb, X_test, y_test, "Tuned XGBoost")
tuned_lgb_auc, tuned_lgb_f1 = evaluate_model_comprehensive(best_lgb, X_test, y_test, "Tuned LightGBM")

# Step 13: Cross-validation scores
print("\n" + "=" * 80)
print("CROSS-VALIDATION SCORES (5-FOLD STRATIFIED)")
print("=" * 80)

cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

xgb_cv_scores = cross_val_score(best_xgb, X_train, y_train, cv=cv_strategy, scoring="roc_auc")
print(f"Tuned XGBoost CV AUC-ROC scores: {xgb_cv_scores}")
print(f"Mean: {xgb_cv_scores.mean():.4f} (+/- {xgb_cv_scores.std() * 2:.4f})")

lgb_cv_scores = cross_val_score(best_lgb, X_train, y_train, cv=cv_strategy, scoring="roc_auc")
print(f"\nTuned LightGBM CV AUC-ROC scores: {lgb_cv_scores}")
print(f"Mean: {lgb_cv_scores.mean():.4f} (+/- {lgb_cv_scores.std() * 2:.4f})")

# Step 14: Final model comparison
print("\n" + "=" * 80)
print("FINAL MODEL COMPARISON")
print("=" * 80)

results = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "XGBoost (Initial)",
        "LightGBM (Initial)",
        "Tuned XGBoost",
        "Tuned LightGBM"
    ],
    "AUC-ROC": [log_auc, xgb_auc, lgb_auc, tuned_xgb_auc, tuned_lgb_auc],
    "F1-Score": [log_f1, xgb_f1, lgb_f1, tuned_xgb_f1, tuned_lgb_f1]
}).sort_values(by="AUC-ROC", ascending=False)

print(results.to_string(index=False))

# Step 15: Feature importance for the best model
print("\n" + "=" * 80)
print("FEATURE IMPORTANCE ANALYSIS")
print("=" * 80)

best_model = best_xgb if tuned_xgb_auc > tuned_lgb_auc else best_lgb
best_model_name = "Tuned XGBoost" if tuned_xgb_auc > tuned_lgb_auc else "Tuned LightGBM"

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": best_model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print(f"\nTop 10 Features (from {best_model_name}):")
print(feature_importance.head(10).to_string(index=False))

# Step 16: Visualization
print("\n" + "=" * 80)
print("GENERATING VISUALIZATIONS")
print("=" * 80)

# Feature Importance Plot
plt.figure(figsize=(12, 8))
sns.barplot(x="Importance", y="Feature", data=feature_importance.head(15), palette="viridis")
plt.title(f"Top 15 Feature Importances ({best_model_name})", fontsize=14)
plt.xlabel("Importance", fontsize=12)
plt.ylabel("Feature", fontsize=12)
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=300, bbox_inches='tight')
print("✓ Feature importance plot saved as 'feature_importance.png'")
plt.close()

# ROC Curve Comparison
plt.figure(figsize=(10, 8))
fpr_xgb, tpr_xgb, _ = roc_curve(y_test, best_xgb.predict_proba(X_test)[:, 1])
fpr_lgb, tpr_lgb, _ = roc_curve(y_test, best_lgb.predict_proba(X_test)[:, 1])
fpr_log, tpr_log, _ = roc_curve(y_test, log_reg.predict_proba(X_test_scaled)[:, 1])

plt.plot(fpr_xgb, tpr_xgb, label=f'Tuned XGBoost (AUC={tuned_xgb_auc:.4f})', linewidth=2)
plt.plot(fpr_lgb, tpr_lgb, label=f'Tuned LightGBM (AUC={tuned_lgb_auc:.4f})', linewidth=2)
plt.plot(fpr_log, tpr_log, label=f'Logistic Regression (AUC={log_auc:.4f})', linewidth=2)
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1)
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('ROC Curve Comparison', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("roc_curve_comparison.png", dpi=300, bbox_inches='tight')
print("✓ ROC curve comparison saved as 'roc_curve_comparison.png'")
plt.close()

# Model Comparison Bar Plot
plt.figure(figsize=(10, 6))
x_pos = np.arange(len(results))
plt.bar(x_pos, results["AUC-ROC"], alpha=0.8, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
plt.xlabel('Model', fontsize=12)
plt.ylabel('AUC-ROC Score', fontsize=12)
plt.title('Model Performance Comparison', fontsize=14)
plt.xticks(x_pos, results["Model"], rotation=45, ha='right')
plt.ylim([0.6, 0.8])
for i, v in enumerate(results["AUC-ROC"]):
    plt.text(i, v + 0.005, f'{v:.4f}', ha='center', va='bottom', fontsize=10)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig("model_comparison.png", dpi=300, bbox_inches='tight')
print("✓ Model comparison plot saved as 'model_comparison.png'")
plt.close()

# Step 17: Save the best model
print("\n" + "=" * 80)
print("SAVING MODELS")
print("=" * 80)

joblib.dump(best_model, "best_model_improved.pkl")
print(f"✓ Best model ({best_model_name}) saved as 'best_model_improved.pkl'")

joblib.dump(scaler, "scaler.pkl")
print("✓ Scaler saved as 'scaler.pkl'")

joblib.dump(smote, "smote.pkl")
print("✓ SMOTE transformer saved as 'smote.pkl'")

# Step 18: Final Summary
print("\n" + "=" * 80)
print("MILESTONE 4 COMPLETION SUMMARY")
print("=" * 80)
print(f"\n✓ Best Model: {best_model_name}")
print(f"✓ Best AUC-ROC Score: {max(results['AUC-ROC']):.4f}")
print(f"✓ Best F1-Score: {results[results['AUC-ROC'] == max(results['AUC-ROC'])]['F1-Score'].values[0]:.4f}")
print(f"✓ Improvement vs Baseline: {((max(results['AUC-ROC']) - log_auc) / log_auc * 100):.2f}%")
print(f"\n✓ All visualizations and models saved successfully!")
print("=" * 80)
