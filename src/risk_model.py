import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

df = pd.read_csv("../data/final_features.csv")

# Clean column names
df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True)

X = df.drop("Status", axis=1)
y = df["Status"]

# --- Data Cleaning ---
# 1. Replace inf/-inf with NaN so they can be handled uniformly
X.replace([np.inf, -np.inf], np.nan, inplace=True)

# 2. Drop rows where any feature is NaN (keeps y aligned)
mask = X.notna().all(axis=1)
X = X[mask]
y = y[mask]

# 3. Clip extreme values to ±1e15 to avoid float64 overflow in StandardScaler
X = X.clip(lower=-1e15, upper=1e15)

print(f"Dataset shape after cleaning: {X.shape}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression(max_iter=2000)

model.fit(X_train, y_train)

pred = model.predict_proba(X_test)[:,1]

print("AUC:", roc_auc_score(y_test, pred))