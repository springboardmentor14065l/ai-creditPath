from __future__ import annotations

import math
import os
from functools import lru_cache
from typing import Any

import joblib
import numpy as np
import pandas as pd


BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

TRAINING_FEATURES_PATH = os.path.join(DATA_DIR, "final_features.csv")
XGB_MODEL_PATH = os.path.join(OUTPUT_DIR, "xgb_tuned_model.pkl")
LGBM_MODEL_PATH = os.path.join(OUTPUT_DIR, "lgbm_tuned_model.pkl")
STACKED_META_PATH = os.path.join(OUTPUT_DIR, "stacked_ensemble_meta.pkl")
ADVANCED_IMPORTANCE_PATH = os.path.join(OUTPUT_DIR, "advanced_feature_importance.csv")

NUMERIC_FIELDS = [
    "year",
    "loan_amount",
    "rate_of_interest",
    "Interest_rate_spread",
    "Upfront_charges",
    "term",
    "property_value",
    "income",
    "Credit_Score",
    "LTV",
    "dtir1",
]

BINARY_FIELDS = [
    "loan_limit_ncf",
    "Gender_Joint",
    "Gender_Male",
    "Gender_SexNotAvailable",
    "approv_in_adv_pre",
    "loan_type_type2",
    "loan_type_type3",
    "loan_purpose_p2",
    "loan_purpose_p3",
    "loan_purpose_p4",
    "Credit_Worthiness_l2",
    "open_credit_opc",
    "business_or_commercial_nobc",
    "Neg_ammortization_not_neg",
    "interest_only_not_int",
    "lump_sum_payment_not_lpsm",
    "construction_type_sb",
    "occupancy_type_pr",
    "occupancy_type_sr",
    "Secured_by_land",
    "total_units_2U",
    "total_units_3U",
    "total_units_4U",
    "credit_type_CRIF",
    "credit_type_EQUI",
    "credit_type_EXP",
    "coapplicant_credit_type_EXP",
    "age_3544",
    "age_4554",
    "age_5564",
    "age_6574",
    "age_25",
    "age_74",
    "submission_of_application_to_inst",
    "Region_NorthEast",
    "Region_central",
    "Region_south",
    "Security_Type_direct",
]

FEATURE_LABELS = {
    "loan_income_ratio": "Loan-to-income ratio",
    "interest_burden": "Interest burden",
    "ltv_risk": "Loan-to-value risk",
    "high_dti_flag": "High debt-to-income flag",
    "Credit_Score": "Credit score",
    "dtir1": "Debt-to-income ratio",
    "loan_amount": "Loan amount",
    "property_value": "Property value",
    "rate_of_interest": "Interest rate",
    "income_loan_interaction": "Income-loan interaction",
    "log_income": "Log income",
}


def sanitize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy()
    cleaned.columns = cleaned.columns.str.replace(r"[^A-Za-z0-9_]+", "", regex=True)
    return cleaned


@lru_cache(maxsize=1)
def load_artifacts() -> dict[str, Any]:
    xgb_model = joblib.load(XGB_MODEL_PATH)
    lgbm_model = joblib.load(LGBM_MODEL_PATH)
    meta_model = joblib.load(STACKED_META_PATH)

    training_df = pd.read_csv(TRAINING_FEATURES_PATH)
    training_df = sanitize_columns(training_df)
    feature_frame = training_df.drop(columns=["Status"])

    medians = feature_frame.median(numeric_only=True).to_dict()
    stds = (
        feature_frame.std(numeric_only=True)
        .replace(0, np.nan)
        .fillna(1.0)
        .to_dict()
    )
    feature_order = list(xgb_model.feature_names_in_)

    importance_df = pd.read_csv(ADVANCED_IMPORTANCE_PATH)
    importance_map = dict(zip(importance_df["Feature"], importance_df["Avg_Importance"]))

    return {
        "xgb_model": xgb_model,
        "lgbm_model": lgbm_model,
        "meta_model": meta_model,
        "feature_order": feature_order,
        "medians": medians,
        "stds": stds,
        "importance_map": importance_map,
    }


def credit_score_bucket_flags(credit_score: float) -> dict[str, int]:
    if credit_score < 580:
        bucket = "Poor"
    elif credit_score < 670:
        bucket = "Average"
    elif credit_score < 740:
        bucket = "Good"
    else:
        bucket = "Excellent"

    return {
        "credit_score_bucket_Poor": int(bucket == "Poor"),
        "credit_score_bucket_Average": int(bucket == "Average"),
        "credit_score_bucket_Good": int(bucket == "Good"),
        "credit_score_bucket_Excellent": int(bucket == "Excellent"),
    }


def build_feature_frame(payload: dict[str, Any]) -> pd.DataFrame:
    row = {field: 0 for field in BINARY_FIELDS}
    row.update(payload)

    frame = pd.DataFrame([row])
    frame = sanitize_columns(frame)

    income = float(frame.at[0, "income"])
    loan_amount = float(frame.at[0, "loan_amount"])
    interest_rate = float(frame.at[0, "rate_of_interest"])
    ltv = float(frame.at[0, "LTV"])
    dti = float(frame.at[0, "dtir1"])
    credit_score = float(frame.at[0, "Credit_Score"])

    frame["loan_income_ratio"] = loan_amount / (income + 1.0)
    frame["interest_burden"] = loan_amount * interest_rate
    frame["ltv_risk"] = ltv / 100.0
    frame["high_dti_flag"] = int(dti > 40)
    frame["log_income"] = math.log1p(income)
    frame["income_loan_interaction"] = income * loan_amount

    for name, value in credit_score_bucket_flags(credit_score).items():
        frame[name] = value

    frame = frame.drop(columns=["income"])
    frame.replace([np.inf, -np.inf], np.nan, inplace=True)

    artifacts = load_artifacts()
    feature_order = artifacts["feature_order"]
    medians = artifacts["medians"]

    for column in feature_order:
        if column not in frame.columns:
            frame[column] = medians.get(column, 0)

    frame = frame[feature_order]
    frame = frame.fillna(value=medians)
    return frame


def classify_risk(probability: float) -> str:
    if probability < 0.3:
        return "Low"
    if probability < 0.6:
        return "Medium"
    return "High"


def recommend_action(probability: float) -> str:
    if probability < 0.3:
        return "Low Risk - Send Reminder"
    if probability < 0.6:
        return "Medium Risk - Call Customer"
    return "High Risk - Immediate Recovery Action"


def urgency_hours(probability: float) -> int:
    if probability < 0.3:
        return 72
    if probability < 0.6:
        return 24
    return 4


def get_top_drivers(feature_frame: pd.DataFrame, limit: int = 3) -> list[dict[str, Any]]:
    artifacts = load_artifacts()
    medians = artifacts["medians"]
    stds = artifacts["stds"]
    importance_map = artifacts["importance_map"]

    rows = []
    for feature in feature_frame.columns:
        raw_value = float(feature_frame.iloc[0][feature])
        baseline = medians.get(feature, 0.0)
        scale = stds.get(feature, 1.0) or 1.0
        importance = float(importance_map.get(feature, 0.0))
        normalized_distance = abs(raw_value - baseline) / scale
        contribution = importance * normalized_distance
        direction = "raises risk" if raw_value >= baseline else "reduces risk"
        rows.append(
            {
                "feature": feature,
                "raw_value": raw_value,
                "direction": direction,
                "contribution": contribution,
            }
        )

    driver_frame = pd.DataFrame(rows)
    top = driver_frame.sort_values("contribution", ascending=False).head(limit)

    drivers: list[dict[str, Any]] = []
    for _, row in top.iterrows():
        drivers.append(
            {
                "feature": row["feature"],
                "label": FEATURE_LABELS.get(row["feature"], row["feature"].replace("_", " ").title()),
                "raw_value": float(row["raw_value"]),
                "direction": row["direction"],
                "contribution": round(float(row["contribution"]), 4),
            }
        )

    return drivers


def score_payload(payload: dict[str, Any]) -> dict[str, Any]:
    artifacts = load_artifacts()
    xgb_model = artifacts["xgb_model"]
    lgbm_model = artifacts["lgbm_model"]
    meta_model = artifacts["meta_model"]

    feature_frame = build_feature_frame(payload)[artifacts["feature_order"]]
    xgb_probability = float(xgb_model.predict_proba(feature_frame)[0][1])
    lgbm_probability = float(lgbm_model.predict_proba(feature_frame)[0][1])
    meta_features = np.array([[xgb_probability, lgbm_probability]])
    probability = float(meta_model.predict_proba(meta_features)[0][1])
    risk = classify_risk(probability)
    action = recommend_action(probability)

    return {
        "probability": round(probability, 4),
        "risk": risk,
        "action": action,
        "urgency_window_hours": urgency_hours(probability),
        "top_risk_drivers": get_top_drivers(feature_frame),
        "model_used": "Stacked Ensemble (XGBoost + LightGBM + Meta Logistic Regression)",
    }


def score_batch(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    scored = []
    for index, payload in enumerate(payloads, start=1):
        prediction = score_payload(payload)
        prediction["borrower_id"] = payload.get("borrower_id", f"borrower_{index}")
        scored.append(prediction)

    ranked = sorted(scored, key=lambda item: item["probability"], reverse=True)
    for rank, item in enumerate(ranked, start=1):
        item["priority_rank"] = rank

    summary = {
        "total_borrowers": len(ranked),
        "high_risk": sum(item["risk"] == "High" for item in ranked),
        "medium_risk": sum(item["risk"] == "Medium" for item in ranked),
        "low_risk": sum(item["risk"] == "Low" for item in ranked),
    }

    return {
        "summary": summary,
        "predictions": ranked,
    }
