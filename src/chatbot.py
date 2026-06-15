import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os
import streamlit as st

# =========================
# GEMINI SETUP
# =========================

# 🔥 BEST PRACTICE (you can replace with your key)

load_dotenv()

genai.configure(api_key=st.secrets["AQ.Ab8RN6LDirkD69zyx1WGGpg5FfXDEHY05_KYiyC
"])


model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# AI FUNCTION (GENAI)
# =========================
def ask_ai(df, question):
    context = f"""
You are a senior business data analyst.

Dataset columns:
{df.columns.tolist()}

Sample data:
{df.head(10).to_string()}

User Question:
{question}

Give:
- clear insights
- reasoning
- business recommendations
"""

    try:
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"


# =========================
# MAIN CHATBOT FUNCTION
# =========================
def answer_question(question, df):

    if df is None:
        return "⚠️ No dataset loaded. Please upload a file first."

    question_lower = question.lower()

    # =========================
    # GREETING HANDLING
    # =========================
    if question_lower in ["hi", "hello", "hey", "hii", "hola"]:
        return """
👋 Hello! I am your AI Business Analyst.

You can ask me:
• Why profit is low
• Show sales analysis
• Best region
• Category insights
"""

    # =========================
    # AI MODE TRIGGER (IMPROVED)
    # =========================
    ai_keywords = [
        "why", "how", "what", "explain",
        "insight", "trend", "analysis",
        "analyze", "summary", "reason",
        "compare", "problem", "issue"
    ]


    # =========================
    # SALES ANALYSIS
    # =========================
    if "sales" in question_lower:
        total_sales = df["Sales"].sum()
        top_region = df.groupby("Region")["Sales"].sum().idxmax()

        return f"""
📊 SALES ANALYSIS

💰 Total Sales: ${total_sales:,.0f}
🏆 Top Region: {top_region}

🧠 Insight:
Sales are concentrated in strong regions, but weaker regions need improvement.
"""

    # =========================
    # PROFIT ANALYSIS
    # =========================
    elif "profit" in question_lower:
        total_profit = df["Profit"].sum()
        worst_region = df.groupby("Region")["Profit"].sum().idxmin()

        return f"""
📈 PROFIT ANALYSIS

💰 Total Profit: ${total_profit:,.0f}
⚠️ Weak Region: {worst_region}

🧠 Insight:
Profit leakage is mainly due to discounting and regional inefficiencies.
"""

    # =========================
    # CATEGORY ANALYSIS
    # =========================
    elif "category" in question_lower:
        top_category = df.groupby("Category")["Sales"].sum().idxmax()

        return f"""
📦 CATEGORY ANALYSIS

🏆 Best Category: {top_category}

🧠 Insight:
Some categories outperform due to demand and pricing advantages.
"""

    # =========================
    # REGION ANALYSIS
    # =========================
    elif "region" in question_lower:
        best_region = df.groupby("Region")["Sales"].sum().idxmax()

        return f"""
🌍 REGION ANALYSIS

🏆 Best Region: {best_region}

🧠 Insight:
Regional performance varies due to demand and discount strategy.
"""
    # =========================
    # AI MODE (FALLBACK)
    # =========================
    if any(word in question_lower for word in ai_keywords):
        return ask_ai(df, question)

    # =========================
    # DEFAULT RESPONSE
    # =========================
    return """
🤖 AI ANALYST

I can help you analyze your business data.

Try asking:
• "tell me about sales"
• "why profit is low"
• "best region"
• "category insights"
"""