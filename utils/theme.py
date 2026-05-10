from __future__ import annotations

from typing import Dict


LIGHT_THEME: Dict[str, str] = {
    "bg": "#F8FAFC",
    "card": "#FFFFFF",
    "text": "#0F172A",
    "muted": "#475569",
    "primary": "#2563EB",
    "accent": "#7C3AED",
    "border": "#E2E8F0",
}

DARK_THEME: Dict[str, str] = {
    "bg": "#0B1220",
    "card": "#111827",
    "text": "#E5E7EB",
    "muted": "#94A3B8",
    "primary": "#3B82F6",
    "accent": "#8B5CF6",
    "border": "#1F2937",
}


def get_theme(mode: str) -> Dict[str, str]:
    return DARK_THEME if mode == "dark" else LIGHT_THEME


def get_global_css(theme: Dict[str, str]) -> str:
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
:root {{
  --bg: {theme['bg']};
  --card: {theme['card']};
  --text: {theme['text']};
  --muted: {theme['muted']};
  --primary: {theme['primary']};
  --accent: {theme['accent']};
  --border: {theme['border']};
}}
.stApp {{
  background: var(--bg);
  color: var(--text);
  transition: background-color .25s ease, color .25s ease;
  font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}}
.stApp, .stApp p, .stApp li, .stApp label, .stApp span,
.stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6 {{
  color: var(--text) !important;
}}
.stCaption, .st-emotion-cache-1c7y2kd, .subtle {{
  color: var(--muted) !important;
}}
.block-container {{
  padding-top: 3rem !important;
  padding-bottom: 1rem !important;
  max-width: 1100px !important;
}}
/* hide the default streamlit top header bar so it doesn't overlap */
header[data-testid="stHeader"] {{
  background: transparent !important;
  height: 0 !important;
  min-height: 0 !important;
}}
[data-testid="stSidebar"] {{
  background: color-mix(in srgb, var(--card) 92%, transparent);
  border-right: 1px solid var(--border);
}}
[data-testid="stSidebar"] * {{
  color: var(--text) !important;
}}
.glass-card {{
  border: 1px solid color-mix(in srgb, var(--border) 70%, transparent);
  border-radius: 20px;
  padding: 24px;
  background: color-mix(in srgb, var(--card) 86%, transparent);
  box-shadow: 0 16px 40px rgba(2, 8, 20, 0.18);
  backdrop-filter: blur(10px);
}}
.gradient-btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  border-radius: 14px;
  padding: 10px 16px;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(90deg, var(--primary), var(--accent));
}}
.saas-chip {{
  display: inline-block;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(90deg, var(--primary), var(--accent));
}}
.chat-wrap {{
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 14px;
  background: var(--card);
}}
.chat-header {{
  position: sticky;
  top: 0;
  z-index: 2;
  margin: -14px -14px 10px -14px;
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
  border-radius: 18px 18px 0 0;
  background: color-mix(in srgb, var(--card) 95%, transparent);
}}
.chat-bubble-user {{
  margin: 8px 0 8px auto;
  border-radius: 16px 16px 4px 16px;
  padding: 10px 12px;
  max-width: 88%;
  color: #fff;
  background: linear-gradient(90deg, var(--primary), var(--accent));
}}
.chat-bubble-assistant {{
  margin: 8px auto 8px 0;
  border: 1px solid var(--border);
  border-radius: 16px 16px 16px 4px;
  padding: 10px 12px;
  max-width: 88%;
  background: color-mix(in srgb, var(--card) 92%, transparent);
}}
.sch-card {{
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 14px;
  margin-bottom: 12px;
  background: var(--card);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  transition: transform .2s ease, box-shadow .2s ease;
}}
.sch-card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 14px 28px rgba(15, 23, 42, 0.16);
}}
.card-topline {{
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}}
.card-rank {{
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
  margin-bottom: 2px;
}}
.card-title {{
  color: var(--text);
  font-size: 17px;
  font-weight: 800;
  line-height: 1.3;
}}
.eligibility-badge {{
  border-radius: 999px;
  padding: 5px 10px;
  color: #fff !important;
  font-size: 12px;
  font-weight: 800;
  white-space: nowrap;
}}
.badge-green {{
  background: #15803d;
}}
.badge-yellow {{
  background: #ca8a04;
}}
.badge-red {{
  background: #dc2626;
}}
.score-row {{
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin: 6px 0 12px 0;
  color: var(--muted);
  font-size: 12px;
  font-weight: 700;
}}
.match-bar {{
  width: 100%;
  height: 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: color-mix(in srgb, var(--card) 85%, transparent);
  overflow: hidden;
}}
.match-fill {{
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
  transform-origin: left;
  animation: growbar 700ms ease;
}}
@keyframes growbar {{
  from {{ transform: scaleX(0.1); opacity: 0.4; }}
  to {{ transform: scaleX(1); opacity: 1; }}
}}
.subtle {{
  color: var(--muted);
  font-size: 13px;
}}
.stButton > button, .stDownloadButton > button {{
  background: var(--card);
  color: var(--text);
  border-radius: 999px;
  border: 1px solid var(--border);
  transition: transform .14s ease, box-shadow .2s ease, background .2s ease;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.16);
}}
.stButton > button[kind="primary"] {{
  border: none;
  color: #fff;
  background: linear-gradient(90deg, var(--primary), var(--accent));
}}
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {{
  color: var(--text) !important;
  background: var(--card) !important;
}}
.login-shell {{
  border-radius: 24px;
  padding: 48px 18px 32px 18px;
  background: radial-gradient(800px 400px at 12% 50%, color-mix(in srgb, var(--primary) 28%, transparent), transparent),
              radial-gradient(700px 380px at 88% 50%, color-mix(in srgb, var(--accent) 22%, transparent), transparent),
              var(--bg);
}}
.login-hero {{
  padding: 24px 0 24px 8px;
}}
.login-logo {{
  font-size: 52px;
  line-height: 1;
  margin-bottom: 12px;
}}
.login-title {{
  font-size: 42px !important;
  font-weight: 800 !important;
  letter-spacing: 0;
  color: var(--text) !important;
  margin: 0 0 8px 0;
}}
.login-tagline {{
  font-size: 18px !important;
  color: var(--muted) !important;
  margin-bottom: 28px;
}}
.login-features {{
  list-style: none;
  padding: 0;
  margin: 0;
}}
.login-features li {{
  font-size: 15px;
  color: var(--text) !important;
  padding: 7px 0;
  border-bottom: 1px solid color-mix(in srgb, var(--border) 60%, transparent);
}}
.login-features li:last-child {{
  border-bottom: none;
}}
.login-card-title {{
  font-size: 24px !important;
  font-weight: 700 !important;
  color: var(--text) !important;
  margin-bottom: 20px;
}}
.login-links {{
  text-align: center;
  margin-top: 14px;
  font-size: 13px;
  color: var(--muted) !important;
}}
.login-links a {{
  color: var(--primary) !important;
  text-decoration: none;
}}
.login-links a:hover {{
  text-decoration: underline;
}}
/* ── Dashboard header ─────────────────────────────────────── */
.dash-header {{
  padding: 8px 0 10px 0;
  margin-bottom: 4px;
}}
.dash-title {{
  font-size: 40px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
  margin-bottom: 4px;
}}
.dash-subtitle {{
  font-size: 15px;
  color: var(--muted);
  margin-bottom: 0;
}}
/* ── Section heading ──────────────────────────────────────── */
.section-heading {{
  font-size: 20px;
  font-weight: 700;
  color: var(--text);
  margin: 20px 0 12px 0;
}}
/* ── Empty state ──────────────────────────────────────────── */
.empty-state {{
  border: 1px dashed color-mix(in srgb, var(--border) 80%, transparent);
  border-radius: 16px;
  padding: 20px 24px;
  color: var(--muted);
  font-size: 15px;
  text-align: center;
  margin: 16px 0;
  background: color-mix(in srgb, var(--card) 60%, transparent);
}}
/* ── Suggested prompts label ──────────────────────────────── */
.prompts-label {{
  font-size: 13px;
  font-weight: 600;
  color: var(--muted) !important;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin: 14px 0 6px 0;
}}
/* ── Query input form ─────────────────────────────────────── */
.stForm {{
  border: none !important;
  padding: 0 !important;
  background: transparent !important;
}}
.stTextInput input {{
  font-size: 15px !important;
  padding: 10px 14px !important;
  border-radius: 12px !important;
  border: 1px solid var(--border) !important;
  background: var(--card) !important;
  color: var(--text) !important;
}}
.stTextInput input:focus {{
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--primary) 20%, transparent) !important;
}}
@media (max-width: 1024px) {{
  .dash-title {{
    font-size: 28px;
  }}
  .sch-card {{
    border-radius: 16px;
  }}
}}
</style>
"""
