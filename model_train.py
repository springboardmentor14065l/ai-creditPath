import pandas as pd
import numpy as np
import joblib

# STEP 1: Load dataset
df = pd.read_csv("data/final_features.csv")

print("Dataset shape:", df.shape)

# STEP 2: Handle infinite and missing values
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

print("Shape after cleaning:", df.shape)

# STEP 3: Split features and target
X = df.drop("default_status", axis=1)
y = df["default_status"]
print("\nTarget distribution:")
print(y.value_counts())

# ✅ SAVE FEATURE NAMES (VERY IMPORTANT FOR API)
feature_names = X.columns.tolist()
joblib.dump(feature_names, "feature_names.pkl")

# STEP 4: Train-test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# STEP 5: Scaling
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ✅ SAVE SCALER
joblib.dump(scaler, "scaler.pkl")

# STEP 6: Train Logistic Regression model
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_scaled, y_train)

# ✅ SAVE MODEL
joblib.dump(model, "model.pkl")

# STEP 7: Predictions
y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]

# STEP 8: Evaluate using AUC-ROC
from sklearn.metrics import roc_auc_score

auc = roc_auc_score(y_test, y_prob)
print("\nAUC-ROC Score:", round(auc, 4))

# STEP 9: Feature Importance
coefficients = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": model.coef_[0]
}).sort_values(by="Coefficient", ascending=False)

print("\nTop 10 Features Influencing Default Risk:\n")
print(coefficients.head(10))

# STEP 10: Create Risk Score (0–100)
df_results = pd.DataFrame({
    "Actual": y_test,
    "Predicted_Prob": y_prob
})

df_results["Risk_Score"] = (df_results["Predicted_Prob"] * 100).round(2)

# STEP 11: Categorize Risk
def categorize_risk(score):
    if score < 30:
        return "Low Risk"
    elif score < 70:
        return "Medium Risk"
    else:
        return "High Risk"

df_results["Risk_Category"] = df_results["Risk_Score"].apply(categorize_risk)

print("\nSample Risk Predictions:\n")
print(df_results.head(10))

# STEP 12: Save results
df_results.to_csv("data/model_predictions.csv", index=False)

print("\n✅ Model training + files saved for API successfully!")
print("\nSample input row for API:\n")
print(X.iloc[0].to_dict())

print("\n=== REAL HIGH RISK SAMPLE ===\n")
print(X[y == 1].iloc[0].to_dict())