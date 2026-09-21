import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def _find_column(df, candidates):
    """Find a column using case-insensitive matching."""
    normalized = {str(col).strip().lower(): col for col in df.columns}

    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]

    return None


def forecast_sales(df):
    date_col = _find_column(
        df,
        ["order date", "order_date", "date", "transaction date", "transaction_date"]
    )

    sales_col = _find_column(
        df,
        ["sales", "revenue", "amount", "total sales"]
    )

    if date_col is None or sales_col is None:
        raise ValueError(
            "Sales forecasting requires a date column and a sales/revenue column."
        )

    data = df[[date_col, sales_col]].copy()

    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    data[sales_col] = pd.to_numeric(data[sales_col], errors="coerce")

    data = data.dropna(subset=[date_col, sales_col])

    if data.empty:
        raise ValueError("No valid date and sales data available for forecasting.")

    daily = (
        data.groupby(date_col)[sales_col]
        .sum()
        .reset_index()
        .sort_values(date_col)
    )

    if len(daily) < 2:
        raise ValueError("At least two dated observations are required for forecasting.")

    daily["days"] = (
        daily[date_col] - daily[date_col].min()
    ).dt.days

    X = daily[["days"]]
    y = daily[sales_col]

    model = LinearRegression()
    model.fit(X, y)

    last_day = daily["days"].max()

    future_30 = pd.DataFrame(
        np.arange(last_day + 1, last_day + 31),
        columns=["days"]
    )

    future_60 = pd.DataFrame(
        np.arange(last_day + 1, last_day + 61),
        columns=["days"]
    )

    prediction_30 = np.maximum(model.predict(future_30), 0)
    prediction_60 = np.maximum(model.predict(future_60), 0)

    return {
        "30_days": float(prediction_30.mean()),
        "60_days": float(prediction_60.mean()),
        "model": "daily_linear_regression",
    }


def forecast_hr_data(df):
    """
    Compatibility wrapper for the HR forecasting path.
    """
    return forecast_sales(df)