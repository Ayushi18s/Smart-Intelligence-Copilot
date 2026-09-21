import streamlit as st
from openai import OpenAI


def get_openrouter_client():
    api_key = st.secrets.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not configured.")

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def generate_ai_business_summary(context):
    """
    Generate a concise business analysis using OpenRouter.
    """

    client = get_openrouter_client()

    prompt = f"""
You are an enterprise business intelligence analyst.

Analyze only the structured analytics data provided below.

{context}

Generate exactly 3 to 5 concise numbered business insights.

Rules:
- Use only facts and numbers explicitly provided in the data.
- Do not invent causes, trends, customer behavior, strategies, or business outcomes.
- Do not make unsupported claims such as "healthy profitability", "stable demand", "effective cross-selling", or "strong growth".
- Clearly distinguish calculated facts from interpretation.
- Mention exact values when useful.
- Keep each insight to 1-2 sentences.
- Use professional business language.
- Do not use markdown tables.
- Do not use backticks.
- Do not use headings.
- Return only the numbered insights.
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional enterprise BI analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()