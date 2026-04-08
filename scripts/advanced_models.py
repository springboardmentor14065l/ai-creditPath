import pandas as pd
import numpy as np
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

def run_advanced_models():
    # 1. Load Data
    data_path = 'data/clean_loans.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    df = pd.read_csv(data_path)
    
    # 2. Split Data
    X = df.drop('default_status', axis=1)
    y = df['default_status']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Dataset Split: Train={len(X_train)}, Test={len(X_test)}")

    # 3. Train Baseline XGBoost
    print("\n--- Training Baseline XGBoost ---")
    xgb_model = xgb.XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
    xgb_model.fit(X_train, y_train)
    
    xgb_probs = xgb_model.predict_proba(X_test)[:, 1]
    xgb_preds = xgb_model.predict(X_test)
    xgb_auc = roc_auc_score(y_test, xgb_probs)
    xgb_acc = accuracy_score(y_test, xgb_preds)
    
    print(f"XGBoost Baseline -> AUC: {xgb_auc:.4f}, Accuracy: {xgb_acc:.4f}")

    # 4. Train Baseline LightGBM
    print("\n--- Training Baseline LightGBM ---")
    lgb_model = lgb.LGBMClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42, verbose=-1)
    lgb_model.fit(X_train, y_train)
    
    lgb_probs = lgb_model.predict_proba(X_test)[:, 1]
    lgb_preds = lgb_model.predict(X_test)
    lgb_auc = roc_auc_score(y_test, lgb_probs)
    lgb_acc = accuracy_score(y_test, lgb_preds)
    
    print(f"LightGBM Baseline -> AUC: {lgb_auc:.4f}, Accuracy: {lgb_acc:.4f}")

    # 5. Hyperparameter Tuning for XGBoost (Best usually)
    print("\n--- Tuning XGBoost ---")
    param_grid = {
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1],
        'n_estimators': [100, 200]
    }
    
    grid_search = GridSearchCV(xgb.XGBClassifier(random_state=42), param_grid, cv=3, scoring='roc_auc', verbose=1)
    grid_search.fit(X_train, y_train)
    
    best_xgb = grid_search.best_estimator_
    print(f"Best XGB Params: {grid_search.best_params_}")
    
    best_xgb_probs = best_xgb.predict_proba(X_test)[:, 1]
    best_xgb_auc = roc_auc_score(y_test, best_xgb_probs)
    print(f"Tuned XGBoost AUC: {best_xgb_auc:.4f}")

    # 6. Save Best Models
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_xgb, 'models/best_xgboost_model.pkl')
    joblib.dump(lgb_model, 'models/best_lightgbm_model.pkl')
    print("Saved tuned XGBoost and baseline LightGBM models to models/")

    # 7. Visualization: Feature Importance
    print("\n--- Generating Feature Importance Plot ---")
    os.makedirs('plots', exist_ok=True)
    importance = pd.DataFrame({'Feature': X.columns, 'Importance': best_xgb.feature_importances_})
    importance = importance.sort_values(by='Importance', ascending=False).head(15)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=importance)
    plt.title('Top 15 Features (Tuned XGBoost)')
    plt.savefig('plots/advanced_feature_importance.png')
    plt.close()
    print("Saved feature importance plot to plots/advanced_feature_importance.png")

    # 8. Comparison with Baseline
    print("\n--- Final Comparison ---")
    print(f"Random Forest (Baseline): AUC=0.7341")
    print(f"XGBoost (Baseline): AUC={xgb_auc:.4f}")
    print(f"LightGBM (Baseline): AUC={lgb_auc:.4f}")
    print(f"XGBoost (Tuned): AUC={best_xgb_auc:.4f}")

if __name__ == "__main__":
    run_advanced_models()
