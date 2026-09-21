import pandas as pd

def normalize_schema(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    mapping = {
        "sales": ["sales", "revenue", "amount"],
        "profit": ["profit"],
        "region": ["region", "state"],
        "category": ["category"],
        "segment": ["segment"],
        "customer name": ["customer name", "customer"],
        "order date": ["order date", "date"]
    }

    for std, variants in mapping.items():
        if std not in df.columns:
            for v in variants:
                if v in df.columns:
                    df[std] = df[v]
                    break
            else:
                df[std] = 0 if std in ["sales","profit"] else "Unknown"

    df["sales"] = pd.to_numeric(df["sales"], errors="coerce").fillna(0)
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce").fillna(0)

    return df