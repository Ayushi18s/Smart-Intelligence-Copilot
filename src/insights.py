def generate_insights(df):

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    best_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    best_category = (
        df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    insights = f"""
### Executive Summary

• Total Sales: ${total_sales:,.0f}

• Total Profit: ${total_profit:,.0f}

• Best Performing Region: {best_region}

• Best Performing Category: {best_category}

### Recommendations

1. Increase investment in {best_category}

2. Expand operations in {best_region}

3. Investigate low-performing products and categories

4. Optimize discounts to improve profitability
"""

    return insights