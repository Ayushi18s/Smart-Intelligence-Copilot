import pandas as pd

def analyze_root_causes(df):

    insights = {}

    # ---------------- HIGH DISCOUNT ANALYSIS ----------------
    high_discount_df = df[df["Discount"] > 0.3].copy()
    insights["high_discount"] = high_discount_df

    discount_impact = high_discount_df["Profit"].sum()

    # ---------------- LOSS MAKING ORDERS ----------------
    loss_df = df[df["Profit"] < 0].copy()
    insights["loss_orders"] = loss_df

    loss_impact = loss_df["Profit"].sum()

    # ---------------- REGION ANALYSIS ----------------
    region_profit = df.groupby("Region")["Profit"].sum().sort_values()
    insights["region_profit"] = region_profit

    weakest_region = region_profit.idxmin()
    strongest_region = region_profit.idxmax()

    # ---------------- CATEGORY ANALYSIS ----------------
    category_profit = df.groupby("Category")["Profit"].sum().sort_values()
    insights["category_profit"] = category_profit

    weakest_category = category_profit.idxmin()

    # ---------------- BUSINESS SUMMARY ----------------
    insights["summary"] = f"""
🧠 ROOT CAUSE ANALYSIS

⚠️ High Discount Impact: ${discount_impact:,.0f}
❌ Loss Orders Impact: ${loss_impact:,.0f}

📉 Weakest Region: {weakest_region}
🏆 Strongest Region: {strongest_region}
📦 Weakest Category: {weakest_category}

🧠 INSIGHT:
Profit leakage is mainly driven by discount-heavy transactions and underperforming regions.

📌 ACTIONS:
• Reduce discount usage in high-risk segments
• Re-evaluate pricing in {weakest_category}
• Strengthen {strongest_region} expansion strategy
"""

    return insights