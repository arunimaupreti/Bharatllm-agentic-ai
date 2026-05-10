from __future__ import annotations

import streamlit as st


def render_login() -> None:
    st.markdown("<div class='login-shell'>", unsafe_allow_html=True)

    # centre the two columns and give them breathing room
    _, left, right, _ = st.columns([0.5, 2.2, 1.8, 0.5], gap="large")

    with left:
        st.markdown(
            """
            <div class='login-hero'>
                <div class='login-logo'>🎓</div>
                <h1 class='login-title'>BharatLLM</h1>
                <p class='login-tagline'>Find the best scholarships using AI</p>
                <ul class='login-features'>
                    <li>✅ &nbsp;Personalised recommendations</li>
                    <li>✅ &nbsp;Government + private scholarships</li>
                    <li>✅ &nbsp;Multilingual support (EN / HI / TA)</li>
                    <li>✅ &nbsp;Real-time deadline tracking</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='login-card-title'>Welcome back</h2>", unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="you@example.com", label_visibility="visible")
        show_password = st.checkbox("Show password", value=False)
        password = st.text_input(
            "Password",
            type="default" if show_password else "password",
            label_visibility="visible",
        )
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        login = st.button("Login", use_container_width=True, type="primary")
        google = st.button("🔵  Continue with Google", use_container_width=True)
        st.markdown(
            "<p class='login-links'><a href='#'>Sign up</a> &nbsp;·&nbsp; <a href='#'>Forgot password?</a></p>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        if login and email and password:
            st.session_state.logged_in = True
            st.rerun()
        elif google:
            st.session_state.logged_in = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
