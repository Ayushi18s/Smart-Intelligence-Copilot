import pandas as pd

def dataset_profile(df):
    return {
        "shape": df.shape,
        "num_cols": df.select_dtypes(include="number").columns.tolist(),
        "cat_cols": df.select_dtypes(include="object").columns.tolist(),
        "missing": df.isna().sum().sum(),
        "columns": list(df.columns)
    }