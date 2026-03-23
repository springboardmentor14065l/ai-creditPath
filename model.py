# STEP 1: Import Libraries
import pandas as pd

# STEP 2: Load Dataset
df = pd.read_csv("final_features.csv")

print("Data Loaded ✅")
print(df.head())

# STEP 3: Define Features and Target
X = df.drop('default_status', axis=1)
y = df['default_status']

# STEP 4: Train-Test Split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# STEP 5: Scaling
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# STEP 6: Train Model
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train, y_train)

# STEP 7: Predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# STEP 8: AUC
from sklearn.metrics import roc_auc_score

auc = roc_auc_score(y_test, y_prob)

print("\n✅ AUC Score:", auc)

# STEP 9: Feature Importance
coeff = pd.DataFrame({
    'Feature': df.drop('default_status', axis=1).columns,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)

print("\nTop Features Increasing Risk:")
print(coeff.head(5))

print("\nTop Features Decreasing Risk:")
print(coeff.tail(5))