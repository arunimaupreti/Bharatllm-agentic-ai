from __future__ import annotations

from typing import Dict

import streamlit as st

from utils.constants import CATEGORIES, DEFAULT_LANGUAGE, EDUCATION_LEVELS, INDIAN_STATES, SUPPORTED_LANGUAGES
from utils.i18n import t


def render_sidebar() -> Dict:
    ui_language = st.session_state.get("ui_language", DEFAULT_LANGUAGE)
    with st.sidebar:
        st.markdown(f"### {t('student_profile', ui_language)}")
        state = st.selectbox(t("state", ui_language), INDIAN_STATES)
        category = st.selectbox(t("category", ui_language), CATEGORIES)
        income = st.number_input(t("income", ui_language), min_value=0, value=250000, step=10000)
        education = st.selectbox(t("education", ui_language), EDUCATION_LEVELS)
        gender = st.selectbox(t("gender", ui_language), ["Not specified", "Male", "Female", "Other"])
        marks = st.slider("Academic marks (%)", min_value=0, max_value=100, value=75)
        age = st.number_input("Age", min_value=0, max_value=100, value=18, step=1)
        nationality = st.selectbox("Nationality", ["Indian", "Other"])
        course_type = st.selectbox("Course type", ["Any", "Engineering", "Medical", "Science", "Arts", "Commerce", "Technical"])
        institute_type = st.selectbox("Institute type", ["Any", "Government", "Private", "AICTE Approved", "UGC Recognized"])
        language = st.selectbox(
            t("language", ui_language),
            list(SUPPORTED_LANGUAGES.keys()),
            index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.get("ui_language", DEFAULT_LANGUAGE)),
        )
        st.session_state.ui_language = language
        st.divider()
        st.markdown(f"### {t('appearance', language)}")
        is_dark = st.toggle(t("dark_mode", language), value=st.session_state.theme_mode == "dark")
        st.session_state.theme_mode = "dark" if is_dark else "light"
        st.divider()
        st.markdown(f"### {t('saved_scholarships', language)}")
        if not st.session_state.bookmarks:
            st.caption(t("no_saved", language))
        else:
            for b in st.session_state.bookmarks[-6:]:
                st.markdown(f"- {b.get('name')}")
    return {
        "state": state,
        "category": category,
        "income": int(income),
        "education_level": education,
        "gender": gender,
        "marks": int(marks),
        "age": int(age),
        "nationality": nationality,
        "course_type": course_type,
        "institute_type": institute_type,
        "language": language,
    }
