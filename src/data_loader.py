import pandas as pd


def load_data(file):

    try:
        df = pd.read_csv(file, encoding="latin1")

    except Exception:
        df = pd.read_csv(file, encoding="cp1252")

    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            errors="coerce"
        )

    return df