from __future__ import annotations

from typing import List

import streamlit as st

from utils.i18n import prompts_for, t


def render_chat_history(chat_history: List[dict], language: str) -> None:
    if not chat_history:
        return
    st.markdown("<div class='chat-wrap'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='chat-header'>"
        f"<strong>{t('conversation', language)}</strong>"
        f"<span class='subtle'> · {t('context_help', language)}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )
    for msg in chat_history:
        bubble_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-assistant"
        st.markdown(f"<div class='{bubble_class}'>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_suggested_prompts(language: str) -> str:
    st.markdown(f"<p class='prompts-label'>{t('suggested_prompts', language)}</p>", unsafe_allow_html=True)
    cols = st.columns(4)
    selected = ""
    for i, prompt in enumerate(prompts_for(language)):
        if cols[i].button(prompt, key=f"prompt_{i}", use_container_width=True):
            selected = prompt
    return selected


def render_query_input(language: str) -> str:
    query = ""
    with st.form("chat_query_form", clear_on_submit=True):
        c1, c2 = st.columns([8, 1])
        with c1:
            text = st.text_input(
                "Query",
                placeholder=t("query_placeholder", language),
                label_visibility="collapsed",
            )
        with c2:
            sent = st.form_submit_button("Send ➤", use_container_width=True)
        if sent and text.strip():
            query = text.strip()
    return query
