import pandas as pd
import google.generativeai as genai

import streamlit as st

# =========================
# GEMINI SETUP
# =========================

# 🔥 BEST PRACTICE (you can replace with your key)


api_key = st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in secrets.toml")
    st.stop()

genai.configure(api_key=api_key)
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
    
    df.columns = df.columns.str.strip()
    question_lower = question.lower()

    # GREETING
    if question_lower in ["hi", "hello", "hey", "hii", "hola"]:
        return "👋 Hello! I am your AI Business Analyst."

    # SALES
    
    if "sales" in question_lower:
        if "Sales" not in df.columns:
            return "❌ Sales column missing"
        total_sales = df["Sales"].sum()
        top_region = df.groupby("Region")["Sales"].sum().idxmax()
        return f"📊 Sales: {total_sales}, Top Region: {top_region}"

    # PROFIT
    if "profit" in question_lower:
        if "Profit" not in df.columns:
            return "❌ Profit column missing"
        if "Region" not in df.columns:
            return "❌ Region column missing"
        total_profit = df["Profit"].sum()
        worst_region = df.groupby("Region")["Profit"].sum().idxmin()
        return f"📈 Profit: {total_profit}, Weak Region: {worst_region}"

    # CATEGORY
    if "category" in question_lower:
        if "Category" not in df.columns:
            return "❌ Category column missing"
        top_category = df.groupby("Category")["Sales"].sum().idxmax()
        return f"📦 Top Category: {top_category}"

    # REGION
    if "region" in question_lower:
        if "Region" not in df.columns:
            return "❌ Region column missing"
        best_region = df.groupby("Region")["Sales"].sum().idxmax()
        return f"🌍 Best Region: {best_region}"

    # AI MODE
    ai_keywords = [
        "why","how","what","explain",
        "insight","analysis","compare","issue"
    ]

    if any(word in question_lower for word in ai_keywords):
        return ask_ai(df, question)

    return "🤖 Ask me about sales, profit, region, or category"

