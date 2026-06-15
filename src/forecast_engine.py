import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_sales(df):

    # ---------------- PREP DATA ----------------
    daily = df.groupby("Order Date")["Sales"].sum().reset_index()
    daily = daily.sort_values("Order Date")

    if len(daily) < 5:
        return {
            "30_days": 0,
            "60_days": 0,
            "message": "Not enough data for forecasting"
        }

    # ---------------- MODEL ----------------
    X = np.arange(len(daily)).reshape(-1, 1)
    y = daily["Sales"].values

    model = LinearRegression()
    model.fit(X, y)

    # ---------------- PREDICTIONS ----------------
    future_30 = model.predict([[len(X) + 30]])[0]
    future_60 = model.predict([[len(X) + 60]])[0]

    trend = "📈 Growing" if future_60 > future_30 else "📉 Declining"

    return {
        "30_days": float(future_30),
        "60_days": float(future_60),
        "trend": trend
    }