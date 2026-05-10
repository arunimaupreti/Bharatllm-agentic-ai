from __future__ import annotations

from datetime import datetime
from typing import Dict, List

import streamlit as st

from utils.i18n import t


STATUS_CLASS = {
    "Highly Recommended": "badge-green",
    "Eligible": "badge-green",
    "Future Eligible": "badge-yellow",
    "Partially Eligible": "badge-yellow",
    "Not Eligible": "badge-red",
}


def _deadline_label(item: Dict) -> str:
    days = item.get("days_to_deadline")
    if days is None:
        try:
            deadline = datetime.strptime(str(item.get("deadline", "")), "%Y-%m-%d")
            days = (deadline - datetime.now()).days
        except Exception:
            return "Deadline not verified"
    if days < 0:
        return "Deadline closed"
    if days <= 30:
        return f"Closing in {days} days"
    return "Applications open"


def _reason_lines(item: Dict) -> List[str]:
    lines = []
    for reason in item.get("matched_criteria", []):
        lines.append(f"+ {reason}")
    for reason in item.get("failed_criteria", []):
        lines.append(f"- {reason}")
    for warning in item.get("eligibility_warnings", []):
        lines.append(f"! {warning}")
    return lines or ["+ Semantic relevance"]


def render_card(item: Dict, rank: int, language: str) -> bool:
    score = min(100.0, max(0.0, float(item.get("match_score", 0))))
    status = item.get("recommendation_type", item.get("eligibility_status", "Eligible"))
    badge_class = STATUS_CLASS.get(status, "badge-yellow")
    confidence = item.get("eligibility_confidence", score)
    deadline_label = _deadline_label(item)

    st.markdown("<div class='sch-card'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='card-topline'>
            <div>
                <div class='card-rank'>#{rank}</div>
                <div class='card-title'>{item.get('name')}</div>
            </div>
            <span class='eligibility-badge {badge_class}'>{status}</span>
        </div>
        <div class='match-bar'><div class='match-fill' style='width:{score}%;'></div></div>
        <div class='score-row'>
            <span>{t('match_score', language)}: {score}%</span>
            <span>Confidence: {confidence}%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if status == "Future Eligible":
        warnings = item.get("eligibility_warnings") or ["You may become eligible later."]
        st.warning(warnings[0])
    elif status == "Not Eligible":
        st.error("Mandatory eligibility criteria do not match.")

    st.markdown(
        f"Income: up to INR {item.get('max_income') or item.get('income_limit') or 'No cap'}  \n"
        f"Education: {item.get('required_education') or item.get('education_level')}  \n"
        f"Category: {item.get('category') or ', '.join(item.get('categories', []))}  \n"
        f"Deadline: {item.get('deadline')} ({deadline_label})"
    )
    st.markdown(f"**{t('benefits', language)}:** {item.get('benefits')}")
    st.markdown(f"**{t('why_recommended', language)}**")
    for line in _reason_lines(item):
        st.markdown(f"- {line}")

    c1, c2 = st.columns(2)
    with c1:
        st.link_button(t("apply", language), item.get("official_link") or item.get("link"), use_container_width=True, type="primary")
    saved = False
    with c2:
        saved = st.button(t("save", language), key=f"save-{item.get('name')}-{rank}", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    return saved
