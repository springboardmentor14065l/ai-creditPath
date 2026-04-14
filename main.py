from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from src.inference_service import score_batch, score_payload


class LoanInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    borrower_id: Optional[str] = Field(default=None, description="Optional borrower identifier for tracking.")
    year: int = Field(..., ge=2000, le=2100)
    loan_amount: float = Field(..., gt=0)
    rate_of_interest: float = Field(..., ge=0)
    Interest_rate_spread: float = Field(..., ge=0)
    Upfront_charges: float = Field(..., ge=0)
    term: float = Field(..., gt=0)
    property_value: float = Field(..., gt=0)
    income: float = Field(..., gt=0)
    Credit_Score: int = Field(..., ge=300, le=900)
    LTV: float = Field(..., ge=0)
    dtir1: float = Field(..., ge=0)

    loan_limit_ncf: int = 0
    Gender_Joint: int = 0
    Gender_Male: int = 0
    Gender_SexNotAvailable: int = 0
    approv_in_adv_pre: int = 0
    loan_type_type2: int = 0
    loan_type_type3: int = 0
    loan_purpose_p2: int = 0
    loan_purpose_p3: int = 0
    loan_purpose_p4: int = 0
    Credit_Worthiness_l2: int = 0
    open_credit_opc: int = 0
    business_or_commercial_nobc: int = 0
    Neg_ammortization_not_neg: int = 0
    interest_only_not_int: int = 0
    lump_sum_payment_not_lpsm: int = 0
    construction_type_sb: int = 0
    occupancy_type_pr: int = 0
    occupancy_type_sr: int = 0
    Secured_by_land: int = 0
    total_units_2U: int = 0
    total_units_3U: int = 0
    total_units_4U: int = 0
    credit_type_CRIF: int = 0
    credit_type_EQUI: int = 0
    credit_type_EXP: int = 0
    coapplicant_credit_type_EXP: int = 0
    age_3544: int = 0
    age_4554: int = 0
    age_5564: int = 0
    age_6574: int = 0
    age_25: int = 0
    age_74: int = 0
    submission_of_application_to_inst: int = 0
    Region_NorthEast: int = 0
    Region_central: int = 0
    Region_south: int = 0
    Security_Type_direct: int = 0


class BatchLoanInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    records: list[LoanInput] = Field(..., min_length=1, max_length=100)


app = FastAPI(
    title="CreditPathAI Recommendation Engine",
    version="6.0.0",
    description=(
        "Milestone 6 API for borrower default risk scoring, business action recommendation, "
        "and explainable risk drivers powering the frontend dashboard."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "CreditPathAI Milestone 5 API is running.",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict")
def predict(data: LoanInput) -> dict:
    return score_payload(data.model_dump())


@app.post("/predict/batch")
def predict_batch(data: BatchLoanInput) -> dict:
    return score_batch([record.model_dump() for record in data.records])
