# src/recommendation.py

def get_recommendation(probability):
    """
    Input: probability of default
    Output: action recommendation
    """

    if probability < 0.3:
        return "Low Risk → Send reminder notification"

    elif probability < 0.7:
        return "Medium Risk → Call borrower and offer flexible payment plan"

    else:
        return "High Risk → Immediate action: escalate to recovery agent"