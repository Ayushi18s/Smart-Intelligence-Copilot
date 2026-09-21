import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from src.schema import normalize_schema
from src.dataset_detector import detect_dataset_type
from src.kpi_engine import generate_kpis
from src.dataset_summary import generate_dataset_summary
from src.anomaly_detector import detect_anomalies
from src.dataset_profile import dataset_profile

import os

def safe_insights_wrapper(df):
    try:
        schema = detect_schema(df)
        insights = generate_autonomous_insights(df, schema)

        if not insights:
            return ["No strong patterns found"]

        return insights[:5]

    except Exception:
        return ["AI engine could not generate reliable insights"]    

def build_insight_pack(df):
    schema = detect_schema(df)

    return {
        "summary": generate_dataset_summary(df),
        "insights": generate_autonomous_insights(df, schema),
        "kpis": detect_kpis(df, schema),
        "anomalies": detect_anomalies(df)
    }

os.environ["OPENROUTER_API_KEY"] = st.secrets[
    "OPENROUTER_API_KEY"
]

st.set_page_config(
    page_title="Smart Intelligence Copilot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.auto_engine import (
    detect_schema,
    detect_kpis,
    auto_top_dimension,
    generate_autonomous_insights
)

def get_top_category(df, cat_col, num_col):
    tmp = df.groupby(cat_col)[num_col].sum().reset_index()
    tmp = tmp.sort_values(num_col, ascending=False).head(10)
    return tmp


def get_best_columns(df):

    ignore_words = [
        "id",
        "row",
        "postal",
        "zip",
        "code"
    ]


    num_cols = [
        c for c in df.select_dtypes(include="number").columns
        if not any(
            w in c.lower()
            for w in ignore_words
        )
    ]


    cat_cols = df.select_dtypes(
        include="str"
    ).columns.tolist()


    return num_cols, cat_cols

def calculate_data_quality(df):

    total_cells = df.shape[0] * df.shape[1]

    missing = df.isna().sum().sum()
    duplicate_rows = df.duplicated().sum()

    missing_pct = (missing / total_cells) * 100 if total_cells else 0
    duplicate_pct = (duplicate_rows / len(df)) * 100 if len(df) else 0

    score = max(0, 100 - missing_pct - duplicate_pct)

    return round(score, 1)

def clean_numeric_series(s):
    s = s.dropna()
    if s.nunique() <= 1:
        return None
    return s

# =========================
# CONFIG
# =========================


# =========================
# IMPORTS
# =========================
from src.data_loader import load_data
from src.insights import generate_insights
from src.chatbot import answer_question
from src.forecast_engine import forecast_sales
from src.ai_analyst import generate_ai_report
from src.pdf_export import generate_pdf
from src.share import generate_share_link
from src.memory import add_memory, get_memory


def forecast_router(df, dataset_type):
    num_cols = df.select_dtypes(include="number").columns.tolist()

    if len(num_cols) == 0:
        return {"status": "error", "message": "No numeric columns found"}

    # ================= HR ROUTE =================
    if dataset_type == "HR":
        preferred = ["salary", "compensation", "bonus", "pay", "income"]

        main_col = next(
            (c for c in df.columns if c.lower() in preferred),
            None
        )

        if main_col is None:
            main_col = num_cols[0]

        return {
            "status": "hr",
            "main_col": main_col
        }

    # ================= BUSINESS ROUTE =================
    main_col = next(
        (c for c in num_cols if "sales" in c.lower() or "revenue" in c.lower()),
        num_cols[0]
    )

    return {
        "status": "business",
        "main_col": main_col
    }


# =========================
# SESSION STATE
# =========================
if "df" not in st.session_state:
    st.session_state.df = None

# =========================
# SAFE DATA ENGINE (VERY IMPORTANT)
# =========================


# =========================
# LOAD DATA
# =========================
import numpy as np

def safe_mode(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    for col in df.columns:

        # only fix missing values, DO NOT convert types blindly
        if df[col].dtype == "object":
            df[col] = df[col].fillna("unknown")

        elif pd.api.types.is_numeric_dtype(df[col]):
            # only fill numeric nulls
            df[col] = df[col].fillna(df[col].median())

    return df

@st.cache_data
def prepare(file):

    # 1️⃣ LOAD DATA
    df = load_data(file) if file else None

    # 2️⃣ FALLBACK DATA (FIXED)
    if df is None or df.empty:
        df = pd.DataFrame({
            "dummy": [1, 2, 3]
        })

    # 3️⃣ CLEAN COLUMN HEADERS
    df.columns = (
        df.columns
        .str.replace("ï»¿", "", regex=True)
        .str.strip()
        .str.lower()
    )

    # 4️⃣ SAFE CLEANING
    df = safe_mode(df)

    return df
    

def safe_insights_wrapper(df):
    try:
        insights = generate_autonomous_insights(df, detect_schema(df))

        if not insights:
            return ["No strong patterns found"]

        return insights[:5]

    except:
        return ["AI engine could not generate reliable insights"]        
def ai_brain(df, query=None):
    return {
        "summary": generate_dataset_summary(df),
        "insights": generate_insights(df),
        "kpis": detect_kpis(df, detect_schema(df)),
        "anomalies": detect_anomalies(df)
    }

# =========================
# STYLE
# =========================
st.markdown("""
<style>

/* MAIN APP */
.stApp {
    background: var(--background-color);
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    top: 10px;
}

/* MAIN PAGE SPACING FIX */
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: inherit;
}

/* GLASS CARDS */
.glass {
    background: rgba(255,255,255,.05);
    backdrop-filter: blur(12px);
    padding: 24px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,.08);
    margin-bottom: 20px;
}

/* HERO */
.hero {
    width: 100%;
    margin-top: -25px;
    margin-bottom: 25px;
    padding: 32px 36px;
    border-radius: 24px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed, #ec4899);
    color: white;
    box-sizing: border-box;
    overflow: visible;
}

/* KPI */
.metric-card {
    padding: 20px;
    border-radius: 18px;
    background: #111827;
    border: 1px solid rgba(255,255,255,.08);
    text-align: center;
}

/* BUTTON */
.stButton button {
    border-radius: 12px;
    height: 50px;
    font-weight: 600;
}

/* UPLOADER */
[data-testid="stFileUploader"] {
    background: transparent;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(0,0,0,0.1);
}

section[data-testid="stSidebar"] {
    width: 320px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER + SETTINGS
# =========================



# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("""
    <style>
    .sidebar-card {
        text-align: center;
        padding: 24px;
        margin-top: -10px;
        margin-bottom: 20px;
        border-radius: 16px;
        background: rgba(99,102,241,0.12);
        border: 1px solid rgba(99,102,241,0.25);
    }

    .sidebar-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #94a3b8;
    }
    </style>

    <div class="sidebar-card">
        <div class="sidebar-title">🧠 Smart AI</div>
        <div class="sidebar-subtitle">Enterprise Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    selected = option_menu(
        menu_title=None,
        options=[
            "Overview",
            "Dashboard",
            "Deep Analytics",
            "AI Copilot",
            "Forecasting",
            "Reports"
        ],
        icons=[
            "house",
            "bar-chart",
            "activity",
            "robot",
            "graph-up",
            "file-earmark-text"
        ],
        default_index=0
    )


# =========================
# OVERVIEW
# =========================

if selected == "Overview":

    st.markdown("""
    <div class='hero'>

    <h1>🧠 Smart Intelligence Copilot</h1>

    <h3>
    AI-Powered Analytics • Forecasting • Insights • Decision Intelligence
    </h3>

    <p>
    Transform raw CSV files into dashboards,
    insights, forecasts and executive reports instantly.
    </p>

    </div>
    """, unsafe_allow_html=True)

    

    st.markdown("""
    ### 🚀 From Raw Data to Business Decisions

    **Smart Intelligence Copilot** transforms structured business data into
    interactive analytics, predictive insights, and executive-ready reports.

    ---

    ### 🔄 Analytics Workflow

    **1. 📂 Upload Data**  
    Upload a CSV dataset and let the platform automatically understand its structure.

    **2. 🛡️ Profile & Validate**  
    Detect dataset type, data quality, numeric features, categorical dimensions, and missing values.

    **3. 📊 Analyze**  
    Explore KPIs, interactive dashboards, trends, dimensions, and business performance.

    **4. 🔮 Predict**  
    Use forecasting and anomaly detection to identify emerging patterns.

    **5. 🤖 Ask AI**  
    Ask questions about your data and receive context-aware business insights.

    **6. 📄 Export**  
    Generate AI-powered executive reports and downloadable outputs.

    ---

    ### ✨ Core Capabilities

    - 📊 Interactive Business Intelligence Dashboard
    - 🧠 AI-Powered Data Analysis & Business Insights
    - 🔮 Forecasting & Trend Analysis
    - 🚨 Anomaly Detection & Alerts
    - 💬 Natural-Language Data Copilot
    - 📈 Automated KPI & Dimension Analysis
    - 📄 Executive Report Generation & PDF Export

    ---

    ### 📁 Supported Business Data

    Sales • Retail • HR • Finance • Marketing • Operations • Customer Analytics

    > **Tip:** Datasets with numeric metrics, categorical dimensions, and date columns provide the richest analytical experience.
    """)
    st.markdown("---")
    st.markdown("## 📂 Start with Your Dataset")

    st.info("""
    Upload a CSV file to unlock:

    • AI Dashboard

    • KPI Detection

    • Forecasting

    • Deep Analytics

    • Executive Reports

    • AI Copilot
    """)
    file = st.file_uploader(
        "Choose a CSV dataset",
        type=["csv"]
    )

    if file:
        st.session_state.df = prepare(file)
        

    # 🔼 MOVE UPLOADER TO TOP

    df = None

    df = st.session_state.df

    if df is not None:

        dataset_type = detect_dataset_type(df)

        st.success(f"Dataset Loaded 🚀 ({dataset_type} Dataset)")
        st.info(f"📂 Dataset Type Detected: {dataset_type}")

        with st.expander("🧠 AI Dataset Understanding", expanded=True):
            st.markdown(generate_dataset_summary(df))


            quality_score = calculate_data_quality(df)

            numeric_cols = len(df.select_dtypes(include="number").columns)
            categorical_cols = len(df.select_dtypes(include="str").columns)

            # =========================
            # DATA QUALITY SECTION
            # =========================

            missing = df.isna().sum().sum()

            st.markdown("## 🛡️ Data Quality Score")

            st.progress(int(quality_score))

            st.markdown(f"""
            <div style="
            padding:20px;
            border-radius:15px;
            background:#e8f5e9;
            font-size:20px;
            font-weight:700;
            color:#1b5e20;
            ">
            Data Quality Score: {quality_score}/100
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 📊 Quick Summary")

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric("Rows", f"{df.shape[0]:,}")
            c2.metric("Columns", df.shape[1])
            c3.metric("Missing Values", f"{missing:,}")
            c4.metric(
                "Numeric Features",
                len(df.select_dtypes(include='number').columns)
            )
            c5.metric(
                "Categorical Features",
                len(df.select_dtypes(include='str').columns)
            )
        st.dataframe(df.head(30))

    else:
        st.markdown("""
        <div class='glass'>

        <h2>🚀 Ready to Analyze Your Data?</h2>

        <p>
        Upload a CSV file and let the AI automatically transform
        raw data into business intelligence.
        </p>

        <hr>

        <h4>✨ What Happens After Upload?</h4>

        ✅ Automatic Dataset Detection

        ✅ AI-Powered KPI Generation

        ✅ Interactive Executive Dashboard

        ✅ Smart Anomaly Detection

        ✅ Forecasting & Trend Analysis

        ✅ AI Chat Assistant

        ✅ Executive Report Generation

        ✅ PDF Export

        <hr>

        <h4>📊 Supported Datasets</h4>

        • Sales Data

        • Retail Data

        • HR Analytics

        • Finance Data

        • Marketing Data

        • Operations Data

        • Customer Data

        <hr>

        <h4>🎯 Best Results</h4>

        Use datasets containing:

        ✔ Numeric metrics

        ✔ Categories

        ✔ Date columns

        ✔ Business KPIs

        </div>
        """, unsafe_allow_html=True)
        

# =========================
# DASHBOARD (POWER BI STYLE)
# =========================
elif selected == "Dashboard":

    df = st.session_state.df
    if df is None:
        st.warning("Upload dataset first")
        st.stop()

    st.markdown("## 📊 Executive Dashboard")

    num_cols, cat_cols = get_best_columns(df)

    # ================= KPI ROW (FIXED) =================

    st.markdown("### KPIs")

    cols = st.columns(4)

    def pick_best_metric(df):

        num_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()


        ignore_words = [
            "id",
            "row",
            "code",
            "postal",
            "zip"
        ]


        num_cols = [
            c for c in num_cols
            if not any(
                w in c.lower()
                for w in ignore_words
            )
        ]


        priority = [
            "sales",
            "revenue",
            "profit",
            "income",
            "salary",
            "amount"
        ]


        for key in priority:
            for col in num_cols:
                if key in col.lower():
                    return col


        return num_cols[0] if num_cols else None

    metric = pick_best_metric(df)

    if metric:
        cols[0].metric("Total", round(df[metric].sum(), 2))
        cols[1].metric("Average", round(df[metric].mean(), 2))
        cols[2].metric("Max", round(df[metric].max(), 2))
        cols[3].metric("Min", round(df[metric].min(), 2))

    # ================= MAIN CHART =================
    num_cols, cat_cols = get_best_columns(df)

    st.markdown("### 📊 Main Insight")

    if len(num_cols) > 0 and len(cat_cols) > 0:

        cat = cat_cols[0]
        num = num_cols[0]

        chart_df = get_top_category(df, cat, num)

        if len(chart_df) > 0:

            st.markdown("### 🔥 Top Categories Impact")

            fig = px.bar(
                chart_df,
                x=cat,
                y=num,
                text=num,
                title=f"Top 10 {cat} by {num}"
            )
            st.plotly_chart(fig, width="stretch")

        # 📈 NEW: Trend line (this makes dashboard feel advanced)
        st.markdown("### 📈 Trend Analysis")

        trend_df = df[num].sort_index().rolling(5).mean()
        
        fig2 = px.line(
            x=trend_df.index,
            y=trend_df.values,
            title=f"{num} Moving Average Trend (5 window)"
        )
        st.plotly_chart(fig2, width="stretch")

    # ================= SECONDARY CHARTS =================
    col1, col2 = st.columns(2)

    if len(num_cols) > 1:

        st.markdown("### 🔥 Correlation Heatmap")

        corr = df[num_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            title="Feature Correlation Matrix"
        )

        st.plotly_chart(fig, width="stretch")

    # ================= AI INSIGHTS =================
    
    # ================= DATA =================
    st.markdown("### 📋 Data Preview")
    st.dataframe(df.head(50))


    # ================= EXTRA POWER BI STYLE CHARTS =================

    st.markdown("## 📊 More Insights (Advanced Charts)")

    # 1️⃣ PIE CHART
    if len(cat_cols) > 0 and len(num_cols) > 0:

        cat = cat_cols[0]
        num = num_cols[0]

        pie_df = df.groupby(cat)[num].sum().reset_index().head(6)

        fig = px.pie(
            pie_df,
            names=cat,
            values=num,
            title=f"{num} Distribution by {cat}"
        )

        st.plotly_chart(fig, width="stretch")

    # 2️⃣ TOP 10 BAR
    if len(num_cols) > 0 and len(cat_cols) > 0:
        top10 = df.groupby(cat_cols[0])[num_cols[0]].sum().nlargest(10).reset_index()

        fig = px.bar(top10, x=cat_cols[0], y=num_cols[0], title="Top 10 Performance")
        st.plotly_chart(fig, width="stretch")

    # 3️⃣ CORRELATION HEATMAP
    if len(num_cols) > 1:
        corr = df[num_cols].corr()

        fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
        st.plotly_chart(fig, width="stretch")

        ignore_words = ["id", "row", "postal", "zip", "code"]

        num_cols = [
            c for c in df.select_dtypes(include="number").columns
            if not any(word in c.lower() for word in ignore_words)
        ]

        cat_cols = df.select_dtypes(include="str").columns.tolist()

        x_col = next((c for c in num_cols if "sales" in c.lower()), num_cols[0])
        y_col = next((c for c in num_cols if "profit" in c.lower()), num_cols[1])

        preferred = ["segment", "category", "region", "ship mode", "sub-category"]

        color_col = None
        for p in preferred:
            for c in cat_cols:
                if c.lower() == p:
                    color_col = c
                    break
            if color_col:
                break

    # 4️⃣ SCATTER RELATIONSHIP
    if len(num_cols) >= 2:
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            opacity=0.65,
            trendline="ols",
            hover_data=df.columns,
            title=f"{y_col} vs {x_col}"
        )

        fig.update_layout(
            height=500,
            legend_title=color_col,
            template="plotly_white"
        )
        st.plotly_chart(fig, width="stretch")

    # 5️⃣ TREND (LINE CHART)
    if len(num_cols) > 0:
        fig = px.line(df.reset_index(), y=num_cols[0], title="Trend Over Data")
        st.plotly_chart(fig, width="stretch")

    # 6️⃣ HISTOGRAM (IMPROVED)
    if len(num_cols) > 0:
        fig = px.histogram(df, x=num_cols[0], nbins=30, title="Distribution Analysis")
        st.plotly_chart(fig, width="stretch")


    # =========================
    # 🔥 PASTE HERE (NEW UPGRADE PACK)
    # =========================


    # =========================
    # 🔥 POWER BI LEVEL INSIGHTS UPGRADE
    # =========================

    st.markdown("## 🚀 Executive Intelligence Layer")

    insight_pack = build_insight_pack(df)

    # 1. INSIGHTS FROM AI
    for i in insight_pack["insights"]:
        st.success("✨ " + i)

    # 2. KPI SUMMARY (from engine)
    st.info(insight_pack["summary"])

    # 3. ANOMALIES
    st.markdown("### 🚨 Anomalies")
    for a in insight_pack["anomalies"]:
        st.warning(a)

    # 4. KPI TABLE
    st.markdown("### 📊 Business KPIs")


    kpi_cols = st.columns(4)


    for idx, item in enumerate(insight_pack["kpis"][:4]):

        title, value = item

        kpi_cols[idx].metric(
            title,
            f"{value:,.2f}"
        )


# =========================
# DEEP ANALYTICS
# =========================
elif selected == "Deep Analytics":

    df = st.session_state.df
    if df is None:
        st.stop()

    st.markdown("### 🧠 AI Insights")
    for i in safe_insights_wrapper(df):
        st.success("✨ " + i)

    st.markdown("### 🚨 Anomaly Detection")

    for item in detect_anomalies(df):
        st.warning(item)

    st.markdown("### 🔍 Advanced Breakdown")

    col1, col2 = st.columns(2)

    with col1:

        ignore_words = ["id", "row", "postal", "zip", "code"]

        num_cols = [
            c for c in df.select_dtypes(include="number").columns
            if not any(word in c.lower() for word in ignore_words)
        ]

        cat_cols = df.select_dtypes(include="str").columns.tolist()

        if len(num_cols) >= 2:

            # Prefer meaningful business metrics
            x_col = next((c for c in num_cols if "sales" in c.lower()), num_cols[0])
            y_col = next((c for c in num_cols if "profit" in c.lower()), num_cols[1])

            preferred = ["segment", "category", "region", "ship mode", "sub-category"]

            color_col = None
            for p in preferred:
                for c in cat_cols:
                    if p.lower() == c.lower():
                        color_col = c
                        break
                if color_col:
                    break

            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                color=color_col,
                opacity=0.7,
                trendline="ols",
                hover_data=df.columns
            )

            fig.update_layout(
                template="plotly_white",
                height=500
            )

            st.plotly_chart(fig, width="stretch")
        
    with col2:

        if "segment" in df.columns:

            metric = None

            for col in num_cols:
                if "sales" in col.lower():
                    metric = col
                    break

            if metric is None:
                for col in num_cols:
                    if "profit" in col.lower():
                        metric = col
                        break

            if metric is None:
                metric = num_cols[0]

            seg = df.groupby("segment")[metric].sum().reset_index()

            fig = px.bar(
                seg,
                x="segment",
                y=metric,
                color="segment",
                text_auto=True,
                title=f"{metric.title()} by Segment"
            )

            st.plotly_chart(fig, width="stretch")

# =========================
# AI COPILOT
# =========================
elif selected == "AI Copilot":

    df = st.session_state.df
    if df is None:
        st.warning("⚠️ Please upload a dataset first from Overview tab")
        st.stop()

    st.title("🤖 AI Copilot — Intelligence Hub")

    # =========================
    # QUICK EXECUTIVE CARDS
    # =========================
    st.markdown("## 📊 EXECUTIVE SNAPSHOT")

    num_cols = df.select_dtypes(include="number").columns.tolist()

    sales_col = next((c for c in num_cols if "sale" in c.lower()), None)
    profit_col = next((c for c in num_cols if "profit" in c.lower()), None)

    # fallback
    sales_col = sales_col or (num_cols[0] if len(num_cols) > 0 else None)
    profit_col = profit_col or (num_cols[1] if len(num_cols) > 1 else None)

    sales = df[sales_col].sum() if sales_col else 0
    profit = df[profit_col].sum() if profit_col else 0
    avg_sales = df[sales_col].mean() if sales_col else 0
    max_profit = df[profit_col].max() if profit_col else 0

    st.markdown("---")

    # =========================
    # SMART INSIGHT PANEL
    # =========================
    st.markdown("## 🧠 AI Intelligence Layer")

    try:
        insights = generate_autonomous_insights(df, detect_schema(df))

        if insights:
            for i in insights:
                st.success("✨ " + i)
        else:
            st.warning("No insights detected — try cleaner data")

    except:
        st.error("AI engine temporarily unavailable")

    st.markdown("---")

    st.markdown("## 🧠 AI Data Story")

    try:
        if sales_col and "region" in df.columns:
            total_sales = df[sales_col].sum()
            best_region = df.groupby("region")[sales_col].sum().idxmax()

            st.info(f"""
            📊 Total Value: {total_sales}
            🌍 Best Region: {best_region}
            📉 Insight: {best_region} generated the highest total sales among regions.
            """)
        else:
            st.info("Dataset analyzed successfully. No structured region/sales pattern found.")
    except:
        st.info("AI story unavailable for this dataset.")
    
    # =========================
    # DATA EXPLORATION WIDGETS
    # =========================
    st.markdown("## 🔍 Explore Your Data Visually")

    col1, col2 = st.columns(2)

    with col1:
        if len(df.columns) >= 2:
            usable_cols = [
                c for c in df.columns
                if not any(
                    word in c.lower()
                    for word in [
                        "id",
                        "code",
                        "postal",
                        "zip"
                    ]
                )
            ]


            # Smart default selections for business datasets
            x_default = (
                usable_cols.index("order date")
                if "order date" in usable_cols
                else 0
            )

            y_default = (
                usable_cols.index("sales")
                if "sales" in usable_cols
                else 0
            )

            x_axis = st.selectbox(
                "X-Axis",
                usable_cols,
                index=x_default
            )

            y_axis = st.selectbox(
                "Y-Axis",
                usable_cols,
                index=y_default
            )

        if x_axis and y_axis:
            fig = px.scatter(df, x=x_axis, y=y_axis, title="Interactive Data Explorer")
            st.plotly_chart(fig, width="stretch")

    with col2:
        if len(num_cols) > 0:
            selected_num = st.selectbox(
                "📊 Numeric Distribution",
                num_cols,
                index=num_cols.index("sales") if "sales" in num_cols else 0
            )

            fig2 = px.histogram(df, x=selected_num, nbins=30, title="Distribution Analysis")
            st.plotly_chart(fig2, width="stretch")

    st.markdown("---")

    # =========================
    # SMART FILTER PANEL
    # =========================
    st.markdown("## 🎛 Smart Filters")

    safe_cols = [c for c in df.columns if df[c].nunique() > 1]

    if not safe_cols:
        safe_cols = df.columns.tolist()

    filter_col = st.selectbox(
        "Select column to filter",
        safe_cols,
        index=safe_cols.index("region") if "region" in safe_cols else 0
    )
    filtered_df = df.copy()

    # NUMERIC COLUMN FILTER
    if pd.api.types.is_numeric_dtype(df[filter_col]):

        min_val = float(df[filter_col].min())
        max_val = float(df[filter_col].max())

        range_val = st.slider(
            "Filter range",
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val)
        )

        filtered_df = df[
            (df[filter_col] >= range_val[0]) &
            (df[filter_col] <= range_val[1])
        ]

    # CATEGORICAL / STRING FILTER
    else:

        options = df[filter_col].dropna().unique().tolist()
        selected_val = st.selectbox("Filter value", ["All"] + options)

        if selected_val != "All":
            filtered_df = df[df[filter_col] == selected_val]

    st.dataframe(filtered_df.head(50))

    # =========================
    # CHAT COPILOT (ENHANCED)
    # =========================
    st.markdown("## 💬 Chat with AI Data Brain")

    q = st.text_input("Ask anything about trends, KPIs, patterns, or anomalies")

    if q:
        def safe_answer(q, df):
            try:
                return answer_question(q, df)
            except:
                return "I cannot process this query safely with current dataset structure."

        ans = safe_answer(q, df)

        add_memory(q, ans)

        st.markdown("### 🤖 AI Response")
        st.success(ans)

        # extra intelligence layer
        st.markdown("### 🧠 Follow-up Suggestions")

        follow_ups = [
            "What is the top performing category?",
            "Show me anomalies in data",
            "What will sales be next month?",
            "Which region is underperforming?",
        ]

        for f in follow_ups:
            st.write("👉 " + f)

        with st.expander("🧠 Conversation Memory"):
            st.write(get_memory())
# =========================
# FORECASTING
# =========================
elif selected == "Forecasting":

    df = st.session_state.df
    if df is None:
        st.stop()

    st.title("📈 Forecasting Engine — AI Prediction Hub")

    dataset_type = detect_dataset_type(df)
    route = forecast_router(df, dataset_type)

    if route["status"] == "error":
        st.warning(route["message"])
        st.stop()

    main_col = route["main_col"]

    st.markdown(f"""
    ## 🧠 Smart Forecast Mode
    📂 Dataset Type: **{dataset_type}**
    🎯 Forecast Target: **{main_col}**
    """)

    # ================= CLEAN KPI SNAPSHOT =================
    st.markdown("## 📊 Forecast Intelligence Snapshot")

    total_value = df[main_col].sum()
    avg_value = df[main_col].mean()

    date_col = None

    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            parsed = pd.to_datetime(df[col], errors="coerce")

            if parsed.notna().mean() >= 0.8:
                date_col = col
                break

    if date_col is not None:
        trend_df = df[[date_col, main_col]].copy()

        trend_df[date_col] = pd.to_datetime(
            trend_df[date_col],
            errors="coerce"
        )

        trend_df[main_col] = pd.to_numeric(
            trend_df[main_col],
            errors="coerce"
        )

        trend_df = trend_df.dropna()

        daily_values = (
            trend_df.groupby(date_col)[main_col]
            .sum()
            .sort_index()
        )

        recent_trend = (
            daily_values.tail(30).mean()
            if len(daily_values) >= 30
            else daily_values.mean()
        )

    else:
        recent_trend = avg_value

    c1, c2, c3 = st.columns(3)
    c1.metric("Total", round(total_value, 2))
    c2.metric("Average", round(avg_value, 2))
    c3.metric("Recent Trend", round(recent_trend, 2))

    # ================= FORECAST ENGINE =================
    from src.forecast_engine import forecast_hr_data

    forecast = forecast_hr_data(df) if dataset_type == "HR" else forecast_sales(df)

    st.markdown("## 🔮 AI Forecast Output")

    col1, col2 = st.columns(2)
    col1.metric("30 Days Forecast", round(forecast["30_days"], 2))
    col2.metric("60 Days Forecast", round(forecast["60_days"], 2))

    # ================= TREND VISUAL =================
    future = pd.DataFrame({
        "period": ["30D", "60D", "90D"],
        "forecast": [
            forecast["30_days"],
            forecast["60_days"],
            forecast["60_days"] * 1.5
        ]
    })

    fig = px.line(future, x="period", y="forecast", markers=True)
    st.plotly_chart(fig, width="stretch")

    # ================= INSIGHTS =================
    if date_col is not None and len(daily_values) > 0:
        baseline_value = daily_values.tail(30).mean()
    else:
        baseline_value = avg_value

    growth = (
        ((forecast["30_days"] - baseline_value) / baseline_value) * 100
        if baseline_value
        else 0
    )
    
    st.markdown("## 🧠 AI Insights")

    st.success(f"Expected growth: {round(growth,2)}%")
    st.success("Trend: " + ("Upward 📈" if growth > 0 else "Downward 📉"))
    st.success("Volatility: " + ("High" if df[main_col].std() > df[main_col].mean()*0.5 else "Stable"))

    # ================= BREAKDOWN =================
    st.markdown("## 🔍 Forecast Drivers")

    if "region" in df.columns:
        fig1 = px.bar(df.groupby("region")[main_col].sum().reset_index(),
                      x="region", y=main_col)
        st.plotly_chart(fig1, width="stretch")

    if "category" in df.columns:
        fig2 = px.pie(df, names="category", values=main_col)
        st.plotly_chart(fig2, width="stretch")

    # ================= DEBUG =================
    with st.expander("🧠 Debug Info"):
        st.write({
            "dataset_type": dataset_type,
            "main_col": main_col,
            "forecast": forecast,
            "rows": len(df)
        })
# =========================
# REPORTS
# =========================
elif selected == "Reports":

    df = st.session_state.df
    if df is None:
        st.stop()

    st.title("📄 AI Executive Report")

    report = generate_ai_report(df)

    st.markdown(report)

    # ================= CLEAN KPI SUMMARY =================
    st.markdown("## 📄 Executive Summary")

    st.info(f"""
    Dataset contains **{df.shape[0]} rows** and **{df.shape[1]} columns**.

    Key highlights:
    - Numeric fields: {len(df.select_dtypes(include='number').columns)}
    - Categorical fields: {len(df.select_dtypes(include='str').columns)}
    - Missing data: {df.isna().sum().sum()} values
    """)
    st.markdown("## 📊 Dataset KPIs")

    ignore_words = [
        "id",
        "row",
        "postal",
        "zip",
        "phone",
        "code"
    ]

    num_cols = [
        c for c in df.select_dtypes(include="number").columns
        if not any(word in c.lower() for word in ignore_words)
    ]

    # remove useless numeric columns
    num_cols = [c for c in num_cols if df[c].nunique() > 5]

    if len(num_cols) == 0:
        st.warning("No meaningful numeric KPIs found.")
    else:
        kpi_data = []

        for col in num_cols:
            series = clean_numeric_series(df[col])

            if series is None:
                continue

            kpi_data.append({
                "Metric": col,
                "Total": round(series.sum(), 2),
                "Average": round(series.mean(), 2),
                "Min": round(series.min(), 2),
                "Max": round(series.max(), 2),
                "Missing %": round(df[col].isna().mean() * 100, 2)
            })

        st.dataframe(pd.DataFrame(kpi_data), width="stretch")
    
    # ================= DATA QUALITY =================
    st.markdown("## 🛡 Data Quality Overview")

    total_cells = df.shape[0] * df.shape[1]
    missing = df.isna().sum().sum()

    quality_score = round((1 - missing / total_cells) * 100, 1) if total_cells else 0

    st.progress(int(quality_score))

    st.success(f"Data Quality Score: {quality_score}/100")

    # ================= DOWNLOAD REPORT =================
    pdf = generate_pdf(report)

    st.download_button(
        "⬇ Download Report",
        data=pdf,
        file_name="AI_Executive_Report.pdf",
        mime="application/pdf"
    )

    # ================= SHARE =================
    if st.button("🔗 Share Report"):
        st.code(generate_share_link())