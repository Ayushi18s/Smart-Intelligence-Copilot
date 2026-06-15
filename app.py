import streamlit as st

if "df" not in st.session_state:
    st.session_state.df = None

df = st.session_state.get("df", None)

st.set_page_config(
    page_title="Smart BI Copilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.recommendations import generate_recommendations
from streamlit_option_menu import option_menu
from src.data_loader import load_data
from src.alerts import generate_alerts
from src.insights import generate_insights
from src.chatbot import answer_question

from src.root_cause_engine import analyze_root_causes
from src.forecast_engine import forecast_sales
from src.ai_analyst import generate_ai_report


from dashboard.charts import (
    sales_trend_chart,
    top_products_chart,
    region_sales_chart,
    category_sales_chart,
    top_customers_chart,
    profit_vs_sales_chart
)

# ==============================
# PAGE CONFIG
# ==============================
st.markdown("""
<style>

/* App background */
body {
    background-color: #0e1117;
}

/* Main container */
.block-container {
    padding: 2rem 3rem;
}

/* Title styling */
h1 {
    font-size: 2.4rem !important;
    font-weight: 700;
}

/* Cards */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 14px;
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg,#4facfe,#00f2fe);
    color: black;
    font-weight: 600;
}
.kpi-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    transition: 0.3s;
}

.kpi-card:hover {
    transform: translateY(-4px);
}

.kpi-title {
    font-size: 14px;
    color: #9ca3af;
}

.kpi-value {
    font-size: 30px;
    font-weight: bold;
    margin-top: 8px;
}           
            

</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
# ==============================
# GLOBAL HEADER (FIX THIS)
# ==============================
st.markdown("""
# 📊 Smart Business Intelligence Copilot
### AI-powered analytics, forecasting & insights platform
---
""")
# ==============================
# LOGIN SYSTEM (GLOBAL)
# ==============================

if "user" in st.session_state and st.session_state.user:
    st.sidebar.success(f"Logged in as {st.session_state.user}")
# ==============================
# FILE UPLOAD
# ==============================

# ==============================
# SIDEBAR NAV
# ==============================
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Overview", "Dashboard", "AI Copilot", "AI Insights", "AI Analyst", "Forecasting", "Reports"],
        icons=["house", "bar-chart", "robot", "lightbulb", "brain", "graph-up", "file-earmark-text"],
        default_index=0
    )

# ==============================
# OVERVIEW
# ==============================
if selected == "Overview":

    st.title("📊 Overview")

    st.markdown("""
    ✔ Analyze business performance  
    ✔ Identify profit leaks  
    ✔ Track KPIs  
    ✔ AI insights  
    ✔ Forecast sales  
    ✔ Generate reports  
    """)

    # ✅ MOVE UPLOAD HERE (IMPORTANT FIX)
    uploaded_file = st.file_uploader(
        "📂 Upload Your Business Dataset",
        type=["csv"]
    )

    st.session_state.df = load_data(uploaded_file) if uploaded_file else None

    if st.session_state.df is not None:
        st.success("Dataset loaded successfully")
        st.write(st.session_state.df.shape)
    else:
        st.info("Upload dataset to start")
    if st.session_state.df is not None:
        st.markdown("### 📊 Quick Summary")

        missing = st.session_state.df.isnull().sum().sum()
        rows = len(st.session_state.df)

        score = max(0, 100 - (missing / max(rows,1) * 100))

        st.markdown("### 🛡️ Data Quality Score")

        st.progress(score / 100)

        st.success(f"Data Quality Score: {score:.1f}/100")

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", len(st.session_state.df))
        col2.metric("Columns", len(st.session_state.df.columns))
        col3.metric("Missing Values", st.session_state.df.isnull().sum().sum())

        st.divider()

        st.markdown("### 👀 Dataset Preview")

        st.dataframe(
            st.session_state.df.head(10),
            use_container_width=True
        )

        st.divider()

        st.markdown("### 📈 Dataset Statistics")

        st.dataframe(
            st.session_state.df.describe(),
            use_container_width=True
        )
    
# ==============================
# DASHBOARD
# ==============================
elif selected == "Dashboard":

    if st.session_state.df is None:
        st.warning("Upload dataset first")
        st.stop()
    
    # ==========================
    # FILTERS
    # ==========================

    st.sidebar.markdown("## 🎯 Dashboard Filters")

    filtered_df = st.session_state.df.copy()

    # Region Filter
    if "Region" in filtered_df.columns:
        regions = ["All"] + list(filtered_df["Region"].dropna().unique())

        selected_region = st.sidebar.selectbox(
            "Region",
            regions
        )

        if selected_region != "All":
            filtered_df = filtered_df[
                filtered_df["Region"] == selected_region
            ]

    # Category Filter
    if "Category" in filtered_df.columns:
        categories = ["All"] + list(filtered_df["Category"].dropna().unique())

        selected_category = st.sidebar.selectbox(
            "Category",
            categories
        )

        if selected_category != "All":
            filtered_df = filtered_df[
                filtered_df["Category"] == selected_category
            ]

    # Segment Filter
    if "Segment" in filtered_df.columns:
        segments = ["All"] + list(filtered_df["Segment"].dropna().unique())

        selected_segment = st.sidebar.selectbox(
            "Segment",
            segments
        )

        if selected_segment != "All":
            filtered_df = filtered_df[
                filtered_df["Segment"] == selected_segment
            ]

    required_cols = ["Sales", "Profit"]
    if not all(col in filtered_df.columns for col in required_cols):
        st.error("Dataset must contain Sales and Profit")
        st.stop()

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = len(filtered_df)
    margin = (total_profit / total_sales * 100) if total_sales else 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Revenue</div>
            <div class="kpi-value">${total_sales:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 Profit</div>
            <div class="kpi-value">${total_profit:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🎯 Margin</div>
            <div class="kpi-value">{margin:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ==========================
    # EXECUTIVE SUMMARY
    # ==========================

    best_region = filtered_df.groupby("Region")["Profit"].sum().idxmax()
    weak_region = filtered_df.groupby("Region")["Profit"].sum().idxmin()

    best_category = filtered_df.groupby("Category")["Profit"].sum().idxmax()
    weak_category = filtered_df.groupby("Category")["Profit"].sum().idxmin()

    st.markdown("## 📊 Executive Summary")

    s1, s2, s3, s4 = st.columns(4)

    s1.success(f"🏆 Best Region\n\n{best_region}")
    s2.info(f"📦 Best Category\n\n{best_category}")
    s3.warning(f"⚠️ Weak Region\n\n{weak_region}")
    s4.error(f"📉 Weak Category\n\n{weak_category}")

    st.divider()

    c1, c2 = st.columns([1,1], gap="large")
    c1.plotly_chart(sales_trend_chart(filtered_df), use_container_width=True)
    c2.plotly_chart(region_sales_chart(filtered_df), use_container_width=True)

    c3, c4 = st.columns([1,1], gap="large")
    c3.plotly_chart(top_products_chart(filtered_df), use_container_width=True)
    c4.plotly_chart(category_sales_chart(filtered_df), use_container_width=True)

    st.divider()

    c5, c6 = st.columns([1,1], gap="large")

    c5.plotly_chart(
        top_customers_chart(filtered_df),
        use_container_width=True
    )

    c6.plotly_chart(
        profit_vs_sales_chart(filtered_df),
        use_container_width=True
    )


    st.subheader("🚨 Alerts")
    alerts = generate_alerts(filtered_df)

    for a in alerts:
        if not a:
            continue
        st.write(a)
    st.divider()

    st.subheader("🤖 AI Recommendations")

    recommendations = generate_recommendations(filtered_df)

    for rec in recommendations:
        st.success(rec)


# ==============================
# AI COPILOT
# ==============================
elif selected == "AI Copilot":

    if st.session_state.df is None:
        st.warning("Upload dataset first")
        st.stop()

    st.subheader("🤖 AI Copilot")

    st.info("Ask: Why profit is low? Best region? Trends?")

    insights = generate_insights(st.session_state.df)
    st.markdown(insights)

    st.divider()

    question = st.text_input("Ask your data")

    if question:
        response = answer_question(question, st.session_state.df)
        st.success(response)
    
    st.markdown("### 🧠 Smart AI Suggestions")
    
    if st.session_state.df is not None:
        if st.button("Generate AI Business Insights"):
            insights = generate_insights(st.session_state.df)
            st.success(insights)

# ==============================
# AI INSIGHTS
# ==============================
elif selected == "AI Insights":

    if st.session_state.df is None:
        st.warning("Upload dataset first")
        st.stop()

    st.title("🧠 Root Cause Analysis")

    insights = analyze_root_causes(st.session_state.df)

    st.dataframe(insights["high_discount"])
    st.dataframe(insights["loss_orders"])

    st.bar_chart(insights["region_profit"])
    st.bar_chart(insights["category_profit"])

    if insights.get("summary"):
        st.info(insights["summary"])

# ==============================
# AI ANALYST
# ==============================
elif selected == "AI Analyst":

    if st.session_state.df is None:
        st.warning("Upload dataset first")
        st.stop()

    st.title("🧠 AI Analyst")

    report = generate_ai_report(st.session_state.df)

    st.markdown(report)

# ==============================
# FORECASTING
# ==============================
elif selected == "Forecasting":

    if st.session_state.df is None:
        st.warning("Upload dataset first")
        st.stop()

    result = forecast_sales(st.session_state.df)

    st.metric("Next 30 Days", f"${float(result['30_days']):,.0f}")
    st.metric("Next 60 Days", f"${float(result['60_days']):,.0f}")

    st.info(result.get("trend", "Unknown"))

    if result.get("trend") == "Growing":
        st.success("🚀 Business trend is positive")
    else:
        st.warning("⚠️ Growth is slowing")

# ==============================
# REPORTS
# ==============================
elif selected == "Reports":

    st.title("📄 Enterprise Reports Center")

    mode = st.radio(
        "Select Mode",
        ["🧠 CEO Mode", "📊 Analyst Mode"]
    )

    report = generate_ai_report(st.session_state.df)

    if mode == "🧠 CEO Mode":
        final_report = "CEO STRATEGIC SUMMARY\n\n" + report
    else:
        final_report = "ANALYTICS REPORT\n\n" + report

    # =========================
    # SHOW REPORT
    # =========================
    st.markdown("### 📊 Generated Report")
    st.markdown(final_report)

    # =========================
    # PDF DOWNLOAD (PUT HERE)
    # =========================
    from src.pdf_export import generate_pdf

    pdf = generate_pdf(final_report)

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf,
        file_name="BI_Report.pdf",
        mime="application/pdf"
    )

    # =========================
    # SHARE LINK
    # =========================
    st.subheader("🔗 Share Dashboard")

    if st.button("Generate Share Link"):
        from src.share import generate_share_link
        link = generate_share_link()
        st.code(link)

    # =========================
    # AI CHAT MEMORY
    # =========================
    st.subheader("💬 AI Chat (Memory Enabled)")

    from src.memory import add_memory, get_memory

    question = st.text_input("Ask report AI")

    if question:
        answer = answer_question(question, st.session_state.df)
        add_memory(question, answer)
        st.success(answer)

    st.markdown("### 🧠 Recent Memory")
    st.write(get_memory())

    st.markdown("---")

    st.markdown(
        """
        <center>
        Smart Business Intelligence Copilot • Built with Python, Streamlit, Plotly & AI
        </center>
        """,
        unsafe_allow_html=True
    )