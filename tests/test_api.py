import atexit
import unittest

import httpx
from main import app


def _print_milestone_header():
    print("Milestone 5: API Test Results\n")
 


def _print_milestone_footer():
    print("\nMilestone 5 Completed Successfully")

_print_milestone_header()
atexit.register(_print_milestone_footer)


def sample_payload(**overrides):
    payload = {
        "borrower_id": "demo-1",
        "year": 2024,
        "loan_amount": 20000,
        "rate_of_interest": 0.09,
        "Interest_rate_spread": 0.02,
        "Upfront_charges": 1200,
        "term": 360,
        "property_value": 250000,
        "income": 50000,
        "Credit_Score": 620,
        "LTV": 82,
        "dtir1": 38,
        "Gender_Male": 1,
        "occupancy_type_pr": 1,
        "credit_type_EXP": 1,
        "submission_of_application_to_inst": 1,
    }
    payload.update(overrides)
    return payload


class CreditPathApiTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        transport = httpx.ASGITransport(app=app)
        self.client = httpx.AsyncClient(transport=transport, base_url="http://testserver")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_predict_endpoint_returns_recommendation(self):
        response = await self.client.post("/predict", json=sample_payload())

        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertGreaterEqual(body["probability"], 0)
        self.assertLessEqual(body["probability"], 1)
        self.assertIn(body["risk"], {"Low", "Medium", "High"})
        self.assertIn("Risk", body["action"])
        self.assertIsInstance(body["top_risk_drivers"], list)
        self.assertEqual(len(body["top_risk_drivers"]), 3)

    async def test_predict_batch_returns_ranked_results(self):
        response = await self.client.post(
            "/predict/batch",
            json={
                "records": [
                    sample_payload(borrower_id="A", Credit_Score=760, income=90000, dtir1=22),
                    sample_payload(borrower_id="B", Credit_Score=580, income=35000, dtir1=48, loan_amount=45000),
                ]
            },
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertEqual(body["summary"]["total_borrowers"], 2)
        self.assertEqual(len(body["predictions"]), 2)
        self.assertGreaterEqual(body["predictions"][0]["probability"], body["predictions"][1]["probability"])
        self.assertEqual(body["predictions"][0]["priority_rank"], 1)

    async def test_predict_validation_rejects_invalid_credit_score(self):
        response = await self.client.post("/predict", json=sample_payload(Credit_Score=1000))

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
