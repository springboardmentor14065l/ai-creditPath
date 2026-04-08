import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# --- Load Data ---
df = pd.read_csv('final_features.csv')

X = df.drop('default_status', axis=1)
y = df['default_status']

# --- Train Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- Save Column Order (critical for API) ---
joblib.dump(list(X.columns), 'feature_columns.pkl')
print(f"Feature columns saved: {list(X.columns)}")

# --- Train XGBoost ---
model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='logloss',
    verbosity=0
)
model.fit(X_train, y_train)

# --- Save Model ---
joblib.dump(model, 'model.pkl')
print("Model saved: model.pkl")

# --- Verify AUC ---
from sklearn.metrics import roc_auc_score
y_prob = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_prob)
print(f"Model AUC-ROC: {auc:.4f}")

print("\nAll artifacts saved. Ready for FastAPI.")
