import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    classification_report
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# 🔹 Load dataset
df = pd.read_csv("final_features.csv")

# 🔹 Split features & target
X = df.drop("default", axis=1)
y = df["default"]

# 🔹 Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔥 Pipeline (Scaler + Model)
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000, class_weight='balanced'))
])

# 🔹 Train model
pipeline.fit(X_train, y_train)

print("\n✅ Model training completed")

# 🔹 Predictions
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

# 🔹 AUC Score
auc = roc_auc_score(y_test, y_prob)
print(f"\n📊 AUC-ROC Score: {auc:.4f}")

# 🔹 Classification Report
print("\n📋 Classification Report:\n")
print(classification_report(y_test, y_pred))

# 🔹 ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
plt.plot([0,1], [0,1], linestyle='--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.savefig("roc_curve.png")
plt.close()

print("📈 ROC curve saved as roc_curve.png")

# 🔹 Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.colorbar()
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix.png")
plt.close()

print("📉 Confusion matrix saved as confusion_matrix.png")

# 🔹 Feature Importance
model = pipeline.named_steps["model"]

coeff_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model.coef_[0]
}).sort_values(by="Coefficient", ascending=False)

print("\n🔺 Top features increasing default risk:\n")
print(coeff_df.head(5))

print("\n🔻 Top features reducing default risk:\n")
print(coeff_df.tail(5))

# 🔥 SAVE MODEL (CRITICAL FOR API)
joblib.dump(pipeline, "model.pkl")

print("\n💾 Model saved as model.pkl")