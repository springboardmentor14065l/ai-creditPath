# =========================
# 1. IMPORT LIBRARIES
# =========================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, precision_recall_curve

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


# =========================
# 2. LOAD DATA
# =========================
df = pd.read_csv("final_features.csv")

X = df.drop("default", axis=1)
y = df["default"]


# =========================
# 3. TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# =========================
# 4. XGBOOST MODEL
# =========================
xgb = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)

xgb.fit(X_train, y_train)


# =========================
# 5. LIGHTGBM MODEL
# =========================
lgbm = LGBMClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    verbose=-1
)

lgbm.fit(X_train, y_train)


# =========================
# 6. PREDICTIONS
# =========================
y_prob_xgb = xgb.predict_proba(X_test)[:, 1]
y_prob_lgbm = lgbm.predict_proba(X_test)[:, 1]

y_pred_xgb = xgb.predict(X_test)
y_pred_lgbm = lgbm.predict(X_test)


# =========================
# 7. AUC SCORE
# =========================
auc_xgb = roc_auc_score(y_test, y_prob_xgb)
auc_lgbm = roc_auc_score(y_test, y_prob_lgbm)

print("XGBoost AUC:", auc_xgb)
print("LightGBM AUC:", auc_lgbm)


# =========================
# 🔥 8. SELECT BEST MODEL
# =========================
if auc_xgb > auc_lgbm:
    best_model = xgb
    best_name = "XGBoost"
    best_prob = y_prob_xgb
    best_pred = y_pred_xgb
else:
    best_model = lgbm
    best_name = "LightGBM"
    best_prob = y_prob_lgbm
    best_pred = y_pred_lgbm

print(f"\n🏆 Best Model: {best_name}")


# =========================
# 9. ROC CURVE
# =========================
fpr, tpr, _ = roc_curve(y_test, best_prob)

plt.figure()
plt.plot(fpr, tpr, label=f'{best_name} AUC={roc_auc_score(y_test, best_prob):.3f}')
plt.plot([0,1], [0,1], linestyle='--')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")

plt.legend()
plt.savefig("roc_curve.png", dpi=300, bbox_inches='tight')
plt.close()


# =========================
# 10. CONFUSION MATRIX
# =========================
cm = confusion_matrix(y_test, best_pred)

plt.figure()
sns.heatmap(cm, annot=True, fmt='d')
plt.title(f"Confusion Matrix ({best_name})")

plt.savefig("confusion_matrix.png", dpi=300, bbox_inches='tight')
plt.close()


# =========================
# 11. PRECISION-RECALL
# =========================
precision, recall, _ = precision_recall_curve(y_test, best_prob)

plt.figure()
plt.plot(recall, precision)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve")

plt.savefig("precision_recall.png", dpi=300, bbox_inches='tight')
plt.close()


# =========================
# 12. FEATURE IMPORTANCE
# =========================
importances = best_model.feature_importances_

feat_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10,6))
plt.barh(feat_df['Feature'][:10], feat_df['Importance'][:10])
plt.gca().invert_yaxis()
plt.title("Top 10 Features")

plt.savefig("feature_importance.png", dpi=300, bbox_inches='tight')
plt.close()


# =========================
# 🔥 13. SAVE MODEL
# =========================
joblib.dump(best_model, "model.pkl")

print("\n💾 Best model saved as model.pkl")