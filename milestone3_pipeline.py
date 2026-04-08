import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import joblib

# Step 1: Load dataset
df = pd.read_csv("final_features.csv")

# Step 2: Drop redundant column
if 'Income' in df.columns:
    df = df.drop(columns=['Income'])

# Step 3: Define features and target
X = df.drop(columns=['Default'])  # 'Default' is the target column
y = df['Default']

# Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 6: Train Logistic Regression model
model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
model.fit(X_train_scaled, y_train)

# Step 7: Evaluate model
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]  # Use probabilities for AUC-ROC
auc_score = roc_auc_score(y_test, y_pred_proba)
print(f"Updated AUC-ROC Score: {auc_score:.4f}")

# Step 8: Feature importance
coefficients = model.coef_[0]
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': coefficients
}).sort_values(by='Coefficient', ascending=False)

# Step 9: Output top features
print("\nTop 10 Features Increasing Default Risk:")
print(feature_importance.head(10))

print("\nTop 10 Features Decreasing Default Risk:")
print(feature_importance.tail(10))

# Step 10: Save preprocessing pipeline and model
pipeline = {
    'scaler': scaler,
    'features': X.columns.tolist()
}
joblib.dump(pipeline, "pipeline.pkl")
print("Pipeline saved as 'pipeline.pkl'")

joblib.dump(model, "model.pkl")
print("Model saved as 'model.pkl'")

def preprocess_data(data):
    # Normalize numerical features
    scaler = MinMaxScaler()
    numerical_features = ['LoanAmount', 'DTIRatio', 'credit_utilization', 'interest_burden', 'loan_income_ratio']
    data[numerical_features] = scaler.fit_transform(data[numerical_features])

    return data