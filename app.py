import os
from datetime import datetime

import streamlit as st

SAMPLE_LEADS = [
    {
        "name": "Jordan Lee",
        "company": "Northwind Analytics",
        "role": "VP Operations",
        "industry": "logistics",
        "pain_point": "manual freight reporting",
    },
    {
        "name": "Samira Khan",
        "company": "Harbor Fintech",
        "role": "Head of Product",
        "industry": "fintech",
        "pain_point": "slow onboarding for SMB clients",
    },
]


def render_template_email(lead: dict, product: str, value_prop: str) -> str:
    return (
        f"Subject: Quick idea for {lead['company']} — {value_prop}\n\n"
        f"Hi {lead['name']},\n\n"
        f"I saw {lead['company']} is scaling {lead['role'].lower()} workflows in {lead['industry']}. "
        f"Teams similar to yours often struggle with {lead['pain_point']}.\n\n"
        f"{product} helps by {value_prop}. "
        f"Would you be open to a 15-minute walkthrough this week?\n\n"
        f"Best,\nAnahita\n\n"
        f"---\n"
        f"(Demo mode — deterministic template; no API keys required.)\n"
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )


def try_llm_email(lead: dict, product: str, value_prop: str) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        prompt = (
            "Write a concise B2B cold email.\n"
            f"Lead: {lead}\n"
            f"Product: {product}\n"
            f"Value prop: {value_prop}\n"
            "Constraints: 120-160 words, friendly, specific, include 1 CTA."
        )
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    except Exception:
        return None


st.set_page_config(page_title="Sales Email Personalization", layout="wide")
st.title("AI-Powered Sales Email Personalization")
st.caption("Working prototype with defaults. Optional: set OPENAI_API_KEY for LLM drafting.")

with st.sidebar:
    st.header("Lead")
    lead_idx = st.selectbox("Choose a sample lead", options=list(range(len(SAMPLE_LEADS))), format_func=lambda i: f"{SAMPLE_LEADS[i]['name']} — {SAMPLE_LEADS[i]['company']}")
    lead = SAMPLE_LEADS[int(lead_idx)]

    st.header("Product")
    product = st.text_input("Product name", value="WorkflowIQ")
    value_prop = st.text_input("Value proposition", value="reduce manual reporting time by ~40%")

st.subheader("Lead profile")
st.json(lead)

st.subheader("Generated email")
llm = try_llm_email(lead, product, value_prop)
email_text = llm or render_template_email(lead, product, value_prop)

st.text_area("", value=email_text, height=280)

st.download_button("Download .txt", data=email_text, file_name="sales_email.txt")
