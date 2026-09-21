from src.dataset_detector import detect_dataset_type


def generate_kpis(df):

    dataset_type = detect_dataset_type(df)

    # =========================
    # HR DATASET
    # =========================
    if dataset_type == "HR":

        employees = len(df)

        salary_col = next(
            (
                c for c in df.columns
                if any(
                    x in c.lower()
                    for x in [
                        "salary",
                        "income",
                        "compensation",
                        "pay",
                        "ctc"
                    ]
                )
            ),
            None
        )

        dept_col = next(
            (
                c for c in df.columns
                if any(
                    x in c.lower()
                    for x in [
                        "department",
                        "dept",
                        "team",
                        "function"
                    ]
                )
            ),
            None
        )

        attrition_col = next(
            (
                c for c in df.columns
                if any(
                    x in c.lower()
                    for x in [
                        "attrition",
                        "termd",
                        "employmentstatus"
                    ]
                )
            ),
            None
        )

        avg_salary = (
            round(df[salary_col].mean(), 2)
            if salary_col else 0
        )

        departments = (
            df[dept_col].nunique()
            if dept_col else 0
        )

        attrition_rate = 0

        if attrition_col:
            attrition_rate = round(
                (
                    df[attrition_col]
                    .astype(str)
                    .str.lower()
                    .eq("yes")
                    .mean()
                ) * 100,
                1
            )

        return {
            "k1": ("Employees", employees),
            "k2": ("Avg Salary", f"{avg_salary:,.0f}"),
            "k3": ("Departments", departments),
            "k4": ("Attrition Rate", f"{attrition_rate}%")
        }

    # =========================
    # SALES DATASET
    # =========================
    else:

        sales = df["sales"].sum()
        profit = df["profit"].sum()
        orders = len(df)

        margin = (
            round((profit / sales) * 100, 1)
            if sales else 0
        )

        return {
            "k1": ("Revenue", f"${sales:,.0f}"),
            "k2": ("Profit", f"${profit:,.0f}"),
            "k3": ("Orders", orders),
            "k4": ("Margin", f"{margin}%")
        }