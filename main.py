from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Credit Risk API is running 🚀"}

# Input schema (ONLY core inputs)
class LoanData(BaseModel):
    age: int
    loanamount: float
    creditscore: float
    monthsemployed: int
    numcreditlines: int
    interestrate: float
    loanterm: int
    dtiratio: float

@app.post("/predict")
def predict(data: LoanData):
    try:

        loan_income_ratio = data.loanamount / 50000   # assume income
        credit_utilization = data.numcreditlines / 10
        interest_burden = data.loanamount * data.interestrate
        employment_stability = data.monthsemployed / 12
        high_dti_flag = 1 if data.dtiratio > 0.4 else 0

        # Credit score buckets
        cs_avg = 1 if 600 <= data.creditscore < 700 else 0
        cs_good = 1 if 700 <= data.creditscore < 750 else 0
        cs_exc = 1 if data.creditscore >= 750 else 0

        log_income = np.log(50000)
        income_loan_interaction = 50000 * data.loanamount

        features = np.array([[
            data.age,
            data.loanamount,
            data.creditscore,
            data.monthsemployed,
            data.numcreditlines,
            data.interestrate,
            data.loanterm,
            data.dtiratio,
            0,0,0,  # education
            0,0,0,  # employment type
            0,0,    # marital
            0,0,    # mortgage, dependents
            0,0,0,0,# loan purpose
            0,      # cosigner
            loan_income_ratio,
            credit_utilization,
            interest_burden,
            employment_stability,
            high_dti_flag,
            cs_avg,
            cs_good,
            cs_exc,
            log_income,
            income_loan_interaction
        ]])

        prediction = model.predict(features)[0]

        return {
            "prediction": int(prediction),
            "result": "Default Risk ❌" if prediction == 1 else "Safe ✅"
        }

    except Exception as e:
        return {"error": str(e)}