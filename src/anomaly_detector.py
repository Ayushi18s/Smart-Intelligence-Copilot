import pandas as pd

def detect_anomalies(df):

    findings = []

    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:

        mean = df[col].mean()
        std = df[col].std()

        if std == 0:
            continue

        anomalies = df[
            (df[col] > mean + 3*std) |
            (df[col] < mean - 3*std)
        ]

        if len(anomalies) > 0:
            findings.append(
                f"⚠ {len(anomalies)} anomalies detected in {col}"
            )

    if not findings:
        findings.append("✅ No major anomalies detected")

    return findings