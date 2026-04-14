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