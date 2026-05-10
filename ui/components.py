"""
ui/components.py — Supplementary UI helpers.

Note: scholarships_to_csv and scholarships_to_pdf live in utils/helpers.py.
      render_card lives in components/cards.py.
      These helpers are kept here for any standalone UI usage.
"""
from __future__ import annotations

import time
from typing import Dict

import streamlit as st


def render_chat(role: str, text: str) -> None:
    """Render a single chat bubble using the correct CSS classes from theme.py."""
    cls = "chat-bubble-user" if role == "user" else "chat-bubble-assistant"
    st.markdown(f"<div class='{cls}'>{text}</div>", unsafe_allow_html=True)


def typing_effect(text: str, delay: float = 0.01) -> None:
    """Animate an assistant response character by character."""
    placeholder = st.empty()
    out = ""
    for ch in text:
        out += ch
        placeholder.markdown(
            f"<div class='chat-bubble-assistant'>{out}</div>",
            unsafe_allow_html=True,
        )
        time.sleep(delay)


def render_scholarship_card(item: Dict, reason: str) -> None:
    """Render a scholarship card using the sch-card CSS class from theme.py."""
    st.markdown(
        f"""
<div class="sch-card">
  <h4>{item.get("name")}</h4>
  <p>{item.get("description", "")}</p>
  <p><b>Eligibility:</b> {item.get("category")} | {item.get("education_level")} | Income up to ₹{item.get("income_limit")}</p>
  <p><b>Benefits:</b> {item.get("benefits")}</p>
  <p><b>Deadline:</b> {item.get("deadline")}</p>
  <p><b>Apply:</b> <a href="{item.get("link")}" target="_blank">{item.get("link")}</a></p>
  <p><span class="saas-chip">Match Score: {item.get("match_score")}%</span></p>
  <p><b>Why recommended:</b> {reason}</p>
</div>
        """,
        unsafe_allow_html=True,
    )
