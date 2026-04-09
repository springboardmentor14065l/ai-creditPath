# src/advanced_model.py

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, roc_auc_score


# -------------------------
# XGBoost Model
# -------------------------
def train_xgboost(X_train, X_test, y_train, y_test):

    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]

    print("XGBoost Accuracy:", accuracy_score(y_test, y_pred))
    print("XGBoost AUC:", roc_auc_score(y_test, y_prob))

    return model


# -------------------------
# LightGBM Model
# -------------------------
def train_lightgbm(X_train, X_test, y_train, y_test):

    model = LGBMClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]

    print("LightGBM Accuracy:", accuracy_score(y_test, y_pred))
    print("LightGBM AUC:", roc_auc_score(y_test, y_prob))

    return model