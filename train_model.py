import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("Loan_default.csv")

# Separate features and target
X = df.drop("Default", axis=1)
y = df["Default"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = RandomForestClassifier()

# Train model
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Check accuracy
accuracy = accuracy_score(y_test, predictions)

print("Model Training Completed")
print("Accuracy:", accuracy)