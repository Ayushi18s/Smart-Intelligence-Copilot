import pandas as pd
import streamlit as st

from src.openrouter_client import generate_ai_business_summary
# -----------------------------
# SCHEMA DETECTION
# -----------------------------

def detect_schema(df):

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )


    numeric = df.select_dtypes(
        include="number"
    ).columns.tolist()


    categorical = df.select_dtypes(
        include="object"
    ).columns.tolist()


    datetime = df.select_dtypes(
        include="datetime"
    ).columns.tolist()


    return {
        "numeric": numeric,
        "categorical": categorical,
        "datetime": datetime
    }



# -----------------------------
# BUSINESS COLUMN RANKING
# -----------------------------

def get_business_metrics(schema):

    priority = [
        "sales",
        "revenue",
        "profit",
        "income",
        "salary",
        "amount",
        "quantity"
    ]


    metrics=[]


    for word in priority:

        for col in schema["numeric"]:

            if word in col.lower():

                metrics.append(col)


    return metrics



# -----------------------------
# KPI ENGINE
# -----------------------------

def detect_kpis(df, schema):

    kpis = []


    # Remove useless numeric columns
    ignore_words = [
        "id",
        "code",
        "postal",
        "zip",
        "row"
    ]


    numeric_cols = [
        c for c in schema["numeric"]
        if not any(
            word in c.lower()
            for word in ignore_words
        )
    ]


    if not numeric_cols:
        return [
            ("Total Rows", len(df))
        ]


    # Business priority
    priority = [
        "sales",
        "revenue",
        "profit",
        "income",
        "quantity",
        "amount"
    ]


    business_cols = []


    for key in priority:
        for col in numeric_cols:
            if key in col.lower():
                business_cols.append(col)


    # fallback
    if not business_cols:
        business_cols = numeric_cols



    # Generate KPIs
    for col in business_cols[:3]:

        kpis.append(
            (
                f"Total {col.title()}",
                round(df[col].sum(),2)
            )
        )


        kpis.append(
            (
                f"Average {col.title()}",
                round(df[col].mean(),2)
            )
        )


    kpis.append(
        (
            "Total Records",
            len(df)
        )
    )


    return kpis

# -----------------------------
# TOP DIMENSION
# -----------------------------

def auto_top_dimension(df, schema):

    metrics = get_business_metrics(schema)

    if not metrics:
        return None, None

    # Prefer meaningful business dimensions over IDs/codes
    preferred_dimensions = [
        "segment",
        "category",
        "region",
        "sub-category",
        "sub category",
        "department",
        "state",
        "city",
        "ship mode",
        "market"
    ]

    ignored_dimensions = [
        "id",
        "row",
        "postal",
        "zip",
        "code",
        "phone",
        "customer",
        "product"
    ]

    categorical = schema["categorical"]

    # First choose a meaningful preferred dimension
    cat = next(
        (
            col for preferred in preferred_dimensions
            for col in categorical
            if col.lower() == preferred
        ),
        None
    )

    # Otherwise choose the first categorical column that does not
    # look like an identifier or code
    if cat is None:
        cat = next(
            (
                col for col in categorical
                if not any(word in col.lower() for word in ignored_dimensions)
            ),
            None
        )

    if cat is None:
        return None, None

    metric = metrics[0]

    result = (
        df.groupby(cat)[metric]
        .sum()
        .sort_values(ascending=False)
    )

    return cat, result


# -----------------------------
# AI INSIGHTS
# -----------------------------

def generate_autonomous_insights(df, schema):

    insights = []

    metrics = get_business_metrics(schema)

    # --------------------------------
    # DETERMINISTIC KPI CALCULATIONS
    # --------------------------------

    for col in metrics[:3]:

        insights.append(
            f"""
📊 {col.title()} Performance

Total: {df[col].sum():,.2f}

Average: {df[col].mean():,.2f}
"""
        )

    # --------------------------------
    # BEST BUSINESS DIMENSION
    # --------------------------------

    if metrics:

        cat, result = auto_top_dimension(df, schema)

        if cat is not None and result is not None and not result.empty:

            top = result.index[0]

            insights.append(
                f"""
🏆 Best Performing {cat.title()}

{top}
based on {metrics[0].title()}
"""
            )

    # --------------------------------
    # DATA QUALITY
    # --------------------------------

    missing = int(df.isna().sum().sum())

    insights.append(
        f"""
🧹 Data Quality

Missing Values:
{missing}
"""
    )

    # --------------------------------
    # REAL AI BUSINESS INTERPRETATION
    # --------------------------------

    try:

        context_parts = []

        for col in metrics[:3]:

            total = df[col].sum()
            average = df[col].mean()

            context_parts.append(
                f"{col.title()}: Total={total:,.2f}, Average={average:,.2f}"
            )

        if metrics:

            cat, result = auto_top_dimension(df, schema)

            if cat is not None and result is not None and not result.empty:

                top = result.index[0]
                top_value = result.iloc[0]

                context_parts.append(
                    f"Top {cat.title()}: {top}, "
                    f"{metrics[0].title()}={top_value:,.2f}"
                )

        context_parts.append(
            f"Total records: {len(df):,}"
        )

        context_parts.append(
            f"Missing values: {missing:,}"
        )

        context = "\n".join(context_parts)

        ai_summary = generate_ai_business_summary(context)

        if ai_summary:

            insights.append(
                f"""
🤖 AI Business Interpretation

{ai_summary}
"""
            )

    except Exception as e:

        st.error(f"OpenRouter AI unavailable: {e}")

    return insights