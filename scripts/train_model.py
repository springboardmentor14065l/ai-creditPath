import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib

# --- PATH CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data')
MODELS_DIR = os.path.join(SCRIPT_DIR, '..', 'models')
PLOTS_DIR = os.path.join(SCRIPT_DIR, '..', 'plots')

# Load data
print("Loading data...")
df = pd.read_csv(os.path.join(DATA_DIR, 'clean_loans.csv'))
X = df.drop(columns=['default_status'])
y = df['default_status']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
print("Training Model...")
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# --- VISUALIZATION 1: Confusion Matrix ---
print("Generating Confusion Matrix...")
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, model.predict(X_test))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Safe', 'Default'], yticklabels=['Safe', 'Default'])
plt.title('Confusion Matrix: Predicted vs Actual')
plt.ylabel('Actual Label')
plt.xlabel('Predicted Label')
plt.savefig(os.path.join(PLOTS_DIR, 'confusion_matrix.png'))
plt.close()

# --- VISUALIZATION 2: Feature Importance ---
print("Generating Feature Importance Graph...")
plt.figure(figsize=(10, 8))
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(12).sort_values().plot(kind='barh', color='skyblue')
plt.title('Top 12 Key Factors Driving Loan Default')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'feature_importance.png'))
plt.close()

# Save model
joblib.dump(model, os.path.join(MODELS_DIR, 'credit_path_model.pkl'))
print(f"\nSuccess! Graphs saved in '{PLOTS_DIR}'.")
print(f"Model saved as '{os.path.join(MODELS_DIR, 'credit_path_model.pkl')}'.")
