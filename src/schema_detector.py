import pandas as pd
def analyze_schema(df):
    return {
        "numeric": list(df.select_dtypes(include="number").columns),
        "categorical": list(df.select_dtypes(include="object").columns),
        "all": list(df.columns)
    }

    numeric_cols = list(
        df.select_dtypes(include=["number"]).columns
    )

    categorical_cols = list(
        df.select_dtypes(include=["object"]).columns
    )

    date_cols = []

    for col in df.columns:
        try:
            converted = pd.to_datetime(
                df[col],
                errors="coerce"
            )

            if converted.notna().sum() > len(df) * 0.5:
                date_cols.append(col)

        except:
            pass

    return {
        "numeric": numeric_cols,
        "categorical": categorical_cols,
        "date": date_cols
    }