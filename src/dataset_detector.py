def detect_dataset_type(df):

    cols = [c.lower() for c in df.columns]

    hr_keywords = [
        "employee",
        "salary",
        "department",
        "attrition",
        "gender",
        "age"
    ]

    sales_keywords = [
        "sales",
        "profit",
        "revenue",
        "region",
        "category"
    ]

    marketing_keywords = [
        "campaign",
        "clicks",
        "ctr",
        "impressions"
    ]

    finance_keywords = [
        "expense",
        "income",
        "budget",
        "cashflow"
    ]

    hr_score = sum(any(k in c for c in cols) for k in hr_keywords)
    sales_score = sum(any(k in c for c in cols) for k in sales_keywords)
    marketing_score = sum(any(k in c for c in cols) for k in marketing_keywords)
    finance_score = sum(any(k in c for c in cols) for k in finance_keywords)

    scores = {
        "HR": hr_score,
        "Sales": sales_score,
        "Marketing": marketing_score,
        "Finance": finance_score
    }

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "General"

    return best