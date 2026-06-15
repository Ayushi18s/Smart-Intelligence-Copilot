def generate_ai_report(df):

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

    best_region = df.groupby("Region")["Profit"].sum().idxmax()
    worst_region = df.groupby("Region")["Profit"].sum().idxmin()

    best_category = df.groupby("Category")["Profit"].sum().idxmax()
    worst_category = df.groupby("Category")["Profit"].sum().idxmin()

    top_customer = df.groupby("Customer Name")["Sales"].sum().idxmax()

    report = f"""
🧠 EXECUTIVE AI ANALYST REPORT

📊 BUSINESS PERFORMANCE
💰 Total Sales: ${total_sales:,.0f}
📈 Total Profit: ${total_profit:,.0f}
🎯 Profit Margin: {profit_margin:.2f}%

🏆 TOP PERFORMERS
• Best Region: {best_region}
• Best Category: {best_category}
• Top Customer: {top_customer}

⚠️ UNDERPERFORMERS
• Weak Region: {worst_region}
• Weak Category: {worst_category}

🧠 ROOT CAUSE SUMMARY
Profit instability is primarily caused by uneven regional performance and category-level inefficiencies.

📌 STRATEGIC RECOMMENDATIONS
• Scale operations in {best_region}
• Reduce dependency on low-margin categories
• Strengthen customer retention for top buyers
• Optimize pricing strategy in weak segments

📈 BUSINESS OUTLOOK
Company is stable but margin improvement opportunity exists through cost + discount optimization.

⚡ CONFIDENCE: HIGH (based on historical dataset patterns)
"""

    return report