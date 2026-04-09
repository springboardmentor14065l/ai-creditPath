def recommend_action(prob):
    if prob < 0.3:
        return "Low Risk - Send Reminder"
    elif prob < 0.6:
        return "Medium Risk - Call Customer"
    else:
        return "High Risk - Immediate Recovery Action"