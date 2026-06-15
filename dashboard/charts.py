import plotly.express as px


# =========================
# 1. SALES TREND
# =========================
def sales_trend_chart(df):

    df["Order Date"] = df["Order Date"].astype(str)

    monthly_sales = (
        df.groupby("Order Date")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        title="Monthly Sales Trend"
    )

    return fig


# =========================
# 2. TOP PRODUCTS
# =========================
def top_products_chart(df):

    top_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Sales"
    )

    return fig


# =========================
# 3. REGION SALES
# =========================
def region_sales_chart(df):

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Sales by Region"
    )

    return fig


# =========================
# 4. CATEGORY SALES
# =========================
def category_sales_chart(df):

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        title="Sales by Category"
    )

    return fig


# =========================
# 5. TOP CUSTOMERS
# =========================
def top_customers_chart(df):

    top_customers = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_customers,
        x="Sales",
        y="Customer Name",
        orientation="h",
        title="Top 10 Customers by Revenue"
    )

    return fig


# =========================
# 6. PROFIT vs SALES
# =========================
def profit_vs_sales_chart(df):

    fig = px.scatter(
        df,
        x="Sales",
        y="Profit",
        color="Category",
        title="Profit vs Sales (Performance Analysis)",
        hover_data=["Product Name", "Region", "Customer Name"]
    )

    return fig