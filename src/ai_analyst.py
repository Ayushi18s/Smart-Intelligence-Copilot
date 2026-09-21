def _find_column(df, candidates):
    """Find a dataframe column using case-insensitive matching."""
    normalized = {str(col).strip().lower(): col for col in df.columns}

    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]

    return None


def generate_ai_report(df):

    sales_col = _find_column(df, ["sales", "revenue", "amount", "total sales"])
    profit_col = _find_column(df, ["profit", "net profit"])
    region_col = _find_column(df, ["region"])
    category_col = _find_column(df, ["category"])
    customer_col = _find_column(df, ["customer name", "customer", "customer_name"])

    required = {
        "sales": sales_col,
        "profit": profit_col,
        "region": region_col,
        "category": category_col,
        "customer": customer_col,
    }

    missing = [name for name, col in required.items() if col is None]

    if missing:
        raise ValueError(
            f"AI report requires these columns: {', '.join(missing)}"
        )

    total_sales = df[sales_col].sum()
    total_profit = df[profit_col].sum()

    profit_margin = (
        (total_profit / total_sales) * 100
        if total_sales
        else 0
    )

    best_region = (
        df.groupby(region_col)[profit_col]
        .sum()
        .idxmax()
    )

    worst_region = (
        df.groupby(region_col)[profit_col]
        .sum()
        .idxmin()
    )

    best_category = (
        df.groupby(category_col)[profit_col]
        .sum()
        .idxmax()
    )

    worst_category = (
        df.groupby(category_col)[profit_col]
        .sum()
        .idxmin()
    )

    top_customer = (
        df.groupby(customer_col)[sales_col]
        .sum()
        .idxmax()
    )

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
Profit performance varies across regions and categories, with differences in aggregated profit contributing to the overall result.

📌 STRATEGIC RECOMMENDATIONS
• Review performance drivers in {best_region}
• Investigate low-profit categories
• Review customer-level sales concentration
• Evaluate pricing, discount, and cost factors affecting profitability

📈 BUSINESS OUTLOOK
Historical dataset results indicate opportunities to improve profitability through regional, category, pricing, discount, and cost analysis.

⚡ CONFIDENCE: HIGH (based on historical dataset calculations)
"""

    return report.strip()
