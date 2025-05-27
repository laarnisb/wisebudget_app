def get_spending_by_category(user_id):
    return {"Food": 150.0, "Bills": 90.0, "Transportation": 60.0, "Shopping": 100.0}

def compare_budget_vs_spending(user_budget, actual_spending):
    result = {}
    for category, planned in user_budget.items():
        spent = actual_spending.get(category, 0)
        result[category] = {
            "planned": planned,
            "spent": spent,
            "difference": planned - spent
        }
    return result