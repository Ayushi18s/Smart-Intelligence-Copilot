def generate_recommendations(df):

    recommendations = []

    if "Category" in df.columns and "Profit" in df.columns:
        best_category = (
            df.groupby("Category")["Profit"]
            .sum()
            .idxmax()
        )

        worst_category = (
            df.groupby("Category")["Profit"]
            .sum()
            .idxmin()
        )

        recommendations.append(
            f"Increase focus on {best_category}"
        )

        recommendations.append(
            f"Improve performance of {worst_category}"
        )

    if "Region" in df.columns and "Profit" in df.columns:

        best_region = (
            df.groupby("Region")["Profit"]
            .sum()
            .idxmax()
        )

        worst_region = (
            df.groupby("Region")["Profit"]
            .sum()
            .idxmin()
        )

        recommendations.append(
            f"Expand operations in {best_region}"
        )

        recommendations.append(
            f"Improve profitability in {worst_region}"
        )

    return recommendations