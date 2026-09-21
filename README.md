# 🧠 Smart Intelligence Copilot

### AI-Powered Business Intelligence & Decision Analytics Platform

Smart Intelligence Copilot is an interactive **AI-powered business intelligence platform** built with Streamlit that transforms structured CSV data into dashboards, KPIs, automated insights, anomaly detection, forecasts, natural-language analysis, and executive-ready reports.

The platform is designed to reduce the manual effort involved in exploring business data by automatically profiling datasets, identifying relevant metrics and dimensions, and combining deterministic analytics with AI-generated business interpretation.

---

## 🚀 What It Does

Upload a CSV dataset and move through an end-to-end analytics workflow:

**Upload Data → Profile & Validate → Analyze → Predict → Ask AI → Export**

The application automatically detects dataset characteristics and provides analytical capabilities based on the available data.

---

## ✨ Key Features

### 📊 Interactive Business Intelligence

* Executive KPI dashboards
* Interactive Plotly visualizations
* Automatic numeric and categorical feature detection
* Business dimension analysis
* Sales, profit, quantity, and other metric analysis
* Region/category/segment-level breakdowns

### 🤖 AI Data Copilot

* Natural-language interaction with business data
* AI-generated business summaries
* Context-aware analytical responses
* Structured business interpretation based on calculated metrics

### 🧠 Automated Intelligence

* Automatic dataset type detection
* Automatic schema detection
* KPI identification
* Data-quality assessment
* Automated business insights
* Root-cause analysis
* Business recommendations

### 🔮 Forecasting

* Date-column detection
* Date-based time-series aggregation
* Daily metric forecasting
* 30-day and 60-day forecast outputs
* Linear Regression forecasting baseline
* Trend and volatility indicators
* Forecast-driver visualizations

### 🚨 Anomaly Detection & Alerts

* Automated anomaly identification
* Metric-level anomaly analysis
* Configurable analytical alerts
* Business-focused exception monitoring

### 📄 Executive Reporting

* AI-generated business reports
* PDF export
* Report generation workflows
* Executive-oriented summaries

### 💬 Additional Capabilities

* Chat memory
* Authentication
* Dataset profiling
* Data sharing workflows
* Scheduled reporting support
* Email reporting support

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │     CSV Dataset      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Data Loading &       │
                         │ Dataset Detection    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Schema & Data        │
                         │ Quality Analysis     │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
             ┌────────────┐  ┌────────────┐  ┌────────────┐
             │ KPI Engine │  │ Analytics  │  │ Anomaly    │
             │            │  │ & Insights │  │ Detection  │
             └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
                   │               │               │
                   └───────────────┼───────────────┘
                                   ▼
                         ┌──────────────────────┐
                         │ Forecasting &        │
                         │ Business Intelligence│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ AI Interpretation    │
                         │ & Data Copilot       │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         ▼                      ▼
                 ┌──────────────┐       ┌──────────────┐
                 │ Interactive  │       │ Executive    │
                 │ Dashboard    │       │ Reports/PDF  │
                 └──────────────┘       └──────────────┘
```

---

## 🧩 Project Structure

```text
Smart-Business-Intelligence-Copilot/
│
├── app.py
├── requirements.txt
├── README.md
│
├── dashboard/
│   └── charts.py
│
├── src/
│   ├── ai_analyst.py
│   ├── alerts.py
│   ├── anomaly_detector.py
│   ├── analyzer.py
│   ├── auth.py
│   ├── auth_db.py
│   ├── auto_engine.py
│   ├── chatbot.py
│   ├── data_loader.py
│   ├── dataset_detector.py
│   ├── dataset_profile.py
│   ├── dataset_summary.py
│   ├── email_reports.py
│   ├── forecast_engine.py
│   ├── insights.py
│   ├── kpi_engine.py
│   ├── memory.py
│   ├── openrouter_client.py
│   ├── pdf_export.py
│   ├── recommendations.py
│   ├── report_generator.py
│   ├── root_cause_engine.py
│   ├── scheduler.py
│   ├── schema.py
│   ├── schema_detector.py
│   └── share.py
│
└── data/
    └── Local datasets only
```

> Local datasets, generated reports, credentials, virtual environments, caches, and other non-source artifacts are excluded from version control.

---

## 🛠️ Tech Stack

### Application

* Python
* Streamlit
* Plotly

### Data & Analytics

* Pandas
* NumPy
* Scikit-learn
* SQL-oriented analytical workflows

### AI

* OpenRouter API
* OpenAI-compatible API interface
* AI-generated business interpretation
* Natural-language data analysis

### Reporting

* PDF generation
* PowerPoint/report workflows
* Email reporting support

---

## 🔮 Forecasting Approach

The forecasting module automatically searches for a suitable date column such as:

* Order Date
* Transaction Date
* Invoice Date
* Timestamp
* Date

For dated datasets, observations are aggregated by date and ordered chronologically before fitting a **Linear Regression** model.

The system generates:

* 30-day forecast
* 60-day forecast
* Recent trend indicator
* Trend direction
* Volatility indicator

Forecast values are constrained to non-negative values because they represent business quantities such as sales or revenue.

> **Note:** The forecasting module currently provides a transparent linear-regression baseline rather than a specialized seasonal forecasting model.

---

## 🔐 Configuration

The application uses Streamlit secrets for API credentials.

Create:

```text
.streamlit/secrets.toml
```

and configure:

```toml
OPENROUTER_API_KEY = "your-api-key"
```

Do **not** commit credentials or secret files to Git.

The repository `.gitignore` excludes local secrets, datasets, virtual environments, generated reports, caches, and other local artifacts.

---

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Ayushi18s/Smart-Business-Intelligence-Copilot.git
cd Smart-Business-Intelligence-Copilot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure your API key

Create:

```text
.streamlit/secrets.toml
```

with:

```toml
OPENROUTER_API_KEY = "your-api-key"
```

### 6. Start the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📁 Supported Data

The platform is designed for structured CSV datasets containing combinations of:

* Numeric business metrics
* Categorical dimensions
* Dates or timestamps
* Business KPIs

Example analytical domains include:

* Sales
* Retail
* Finance
* HR
* Marketing
* Operations
* Customer analytics

The platform adapts its analysis based on the structure and available fields in the uploaded dataset.

---

## 🧪 Example Dataset

The application can be tested locally with a retail/sales dataset containing fields such as:

```text
Order Date
Region
Category
Sales
Profit
Quantity
```

For example, a Superstore-style dataset can produce:

* Revenue trends
* Profitability analysis
* Regional performance
* Category analysis
* KPI summaries
* Anomaly detection
* Forecasting
* AI-generated business interpretation

**Datasets are intentionally not included in the public repository.**

---

## 🎯 Design Goals

Smart Intelligence Copilot focuses on four principles:

**Automation**
Reduce repetitive data exploration and manual KPI preparation.

**Interpretability**
Combine calculated metrics with clearly separated AI-generated interpretation.

**Adaptability**
Support different structured business datasets without requiring a fixed schema.

**Decision Support**
Turn raw analytical outputs into dashboards, insights, forecasts, and executive-ready reports.

---

## 🔭 Future Improvements

Potential future enhancements include:

* More advanced time-series forecasting models
* Seasonality and trend decomposition
* Automated feature engineering
* Expanded natural-language analytical querying
* Database connectors
* Real-time data sources
* Role-based access control
* Advanced report customization
* Model evaluation and forecast confidence intervals

---

## 👩‍💻 Author

**Ayushi**

B.Tech — Computer Science & Engineering (Data Science)

GitHub: `Ayushi18s`

---

## 📜 License

This project is intended as a portfolio and demonstration project.
