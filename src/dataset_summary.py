from src.dataset_detector import detect_dataset_type

def generate_dataset_summary(df):

    dataset_type = detect_dataset_type(df)

    summary = []

    summary.append(f"📂 Dataset Type: {dataset_type}")
    summary.append(f"📊 Rows: {len(df)}")
    summary.append(f"📋 Columns: {len(df.columns)}")

    cols = [c.lower() for c in df.columns]

    if dataset_type == "HR":

        if any("salary" in c for c in cols):
            summary.append("💰 Salary column detected")

        if any("attrition" in c for c in cols):
            summary.append("🚪 Attrition column detected")

        summary.append("🧠 Recommended Analysis:")
        summary.append("- Attrition Analysis")
        summary.append("- Workforce Trends")
        summary.append("- Salary Distribution")

    elif dataset_type == "Sales":

        summary.append("🧠 Recommended Analysis:")
        summary.append("- Revenue Trends")
        summary.append("- Profitability Analysis")
        summary.append("- Regional Performance")

    return "\n".join(summary)