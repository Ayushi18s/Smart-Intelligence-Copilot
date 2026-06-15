import numpy as np

def generate_alerts(df):

    alerts = []

    if df is None or len(df) == 0:
        return ["No data available"]

    # ---------------- CLEAN DATA ----------------
    df = df.copy()

    for col in ["Sales", "Profit"]:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # ---------------- LOSS ANALYSIS ----------------
    if "Product" in df.columns and "Profit" in df.columns:

        loss_df = df[df["Profit"] < 0]

        if len(loss_df) > 0:

            top_loss = (
                loss_df.groupby("Product")["Profit"]
                .sum()
                .sort_values()
                .head(5)
            )

            severity = min(10, int(len(loss_df) / 50) + 3)

            alerts.append(
                f"🧠 LOSS ANALYSIS (Severity {severity}/10): "
                f"{len(loss_df)} loss-making transactions detected"
            )

            for product, profit in top_loss.items():
                alerts.append(
                    f"• {product}: total loss ${abs(profit):,.0f}"
                )

            alerts.append(
                "💡 Insight: Losses are concentrated in a few products. "
                "Likely causes: over-discounting or poor product demand."
            )

            alerts.append(
                "📌 Action: Review pricing strategy for top loss-making products."
            )

    # ---------------- MARGIN ANALYSIS ----------------
    if "Sales" in df.columns and "Profit" in df.columns:

        total_sales = df["Sales"].sum()
        total_profit = df["Profit"].sum()

        if total_sales > 0:

            margin = (total_profit / total_sales) * 100

            if margin < 10:

                severity = min(10, int((10 - margin) * 1.2))

                alerts.append(
                    f"🧠 LOW PROFIT MARGIN (Severity {severity}/10): "
                    f"{margin:.2f}% overall margin"
                )

                alerts.append(
                    "💡 Insight: Costs or discounts are eating into profitability."
                )

                alerts.append(
                    "📌 Action: Optimize discounting and reduce low-margin sales."
                )

    # ---------------- DISCOUNT ANALYSIS ----------------
    if "Discount" in df.columns:

        high_discount = df[df["Discount"] > 0.5]

        if len(high_discount) > 0:

            revenue_risk = high_discount["Sales"].sum()
            profit_impact = high_discount["Profit"].sum()

            severity = min(10, int(len(high_discount) / 100) + 4)

            alerts.append(
                f"🧠 HIGH DISCOUNT RISK (Severity {severity}/10): "
                f"{len(high_discount)} transactions impacted"
            )

            alerts.append(
                f"💰 Revenue at risk: ${revenue_risk:,.0f} | "
                f"Profit impact: ${profit_impact:,.0f}"
            )

            alerts.append(
                "💡 Insight: Heavy discounting is reducing profitability."
            )

            alerts.append(
                "📌 Action: Cap discount levels and review discount policy."
            )

    return alerts