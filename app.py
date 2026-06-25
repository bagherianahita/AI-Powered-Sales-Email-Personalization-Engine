"""Streamlit demo — personalized B2B sales emails (no API keys required)."""

from __future__ import annotations

import os
from datetime import datetime

import streamlit as st

DEFAULT_PORT = 8504

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
    {
        "name": "Alex Rivera",
        "company": "Summit Health",
        "role": "Director of IT",
        "industry": "healthcare",
        "pain_point": "disconnected patient intake workflows",
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


st.set_page_config(
    page_title="Sales Email Personalization",
    page_icon="✉️",
    layout="wide",
)

st.title("AI-Powered Sales Email Personalization")
st.caption(
    f"Working prototype with sample leads and instant email drafts. "
    f"Optional: set `OPENAI_API_KEY` for LLM-generated copy."
)

with st.sidebar:
    st.header("Lead")
    lead_idx = st.selectbox(
        "Choose a sample lead",
        options=list(range(len(SAMPLE_LEADS))),
        format_func=lambda i: f"{SAMPLE_LEADS[i]['name']} — {SAMPLE_LEADS[i]['company']}",
    )
    lead = SAMPLE_LEADS[int(lead_idx)]

    st.header("Product")
    product = st.text_input("Product name", value="WorkflowIQ")
    value_prop = st.text_input(
        "Value proposition",
        value="reduce manual reporting time by ~40%",
    )

    use_llm = st.toggle("Use OpenAI (if key set)", value=False)
    generate = st.button("Generate email", type="primary", use_container_width=True)

col_profile, col_email = st.columns([1, 2])

with col_profile:
    st.subheader("Lead profile")
    st.json(lead)

with col_email:
    st.subheader("Generated email")

    if generate or "email_text" not in st.session_state:
        llm = try_llm_email(lead, product, value_prop) if (use_llm and generate) else None
        if llm:
            st.session_state.email_text = llm
            st.session_state.email_mode = "openai"
        else:
            st.session_state.email_text = render_template_email(lead, product, value_prop)
            st.session_state.email_mode = "template"
        st.session_state.lead_key = f"{lead_idx}|{product}|{value_prop}"

    elif st.session_state.get("lead_key") != f"{lead_idx}|{product}|{value_prop}":
        st.session_state.email_text = render_template_email(lead, product, value_prop)
        st.session_state.email_mode = "template"
        st.session_state.lead_key = f"{lead_idx}|{product}|{value_prop}"

    mode = st.session_state.get("email_mode", "template")
    if mode == "openai":
        st.success("Generated with OpenAI")
    else:
        st.info("Demo mode — template email (no API keys)")

    st.code(st.session_state.email_text, language=None)

    st.download_button(
        "Download .txt",
        data=st.session_state.email_text,
        file_name=f"sales_email_{lead['company'].replace(' ', '_').lower()}.txt",
        use_container_width=True,
    )

st.divider()
st.markdown(
    f"**Run locally:** `streamlit run app.py` → http://localhost:{DEFAULT_PORT} "
    f"(or pass `--server.port 8502` if 8504 is busy)"
)
