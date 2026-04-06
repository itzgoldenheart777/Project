import streamlit as st
import pandas as pd

MEESHO_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 40" width="110" height="32">
  <defs>
    <linearGradient id="mg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%"   stop-color="#E91E8C"/>
      <stop offset="100%" stop-color="#FF5252"/>
    </linearGradient>
  </defs>
  <rect width="140" height="40" rx="6" fill="url(#mg)"/>
  <text x="14" y="27" font-family="Arial,sans-serif" font-weight="900"
        font-size="19" fill="#ffffff" letter-spacing="-0.5">meesho</text>
  <circle cx="122" cy="20" r="8" fill="rgba(255,255,255,0.25)"/>
  <text x="115" y="25" font-family="Arial,sans-serif" font-weight="900"
        font-size="13" fill="#ffffff">m</text>
</svg>"""

AMAZON_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 40" width="110" height="32">
  <rect width="140" height="40" rx="6" fill="#131921"/>
  <text x="12" y="22" font-family="Arial,sans-serif" font-weight="900"
        font-size="16" fill="#ffffff" letter-spacing="-0.3">amazon</text>
  <path d="M12 30 Q50 38 88 30" stroke="#FF9900" stroke-width="2.5"
        fill="none" stroke-linecap="round"/>
  <polygon points="84,27 90,30 84,33" fill="#FF9900"/>
</svg>"""

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Manrope, sans-serif", color="#8A94A6", size=12),
    margin=dict(l=10, r=10, t=32, b=10),
    xaxis=dict(
        gridcolor="rgba(46,58,78,0.5)",
        linecolor="rgba(46,58,78,0.6)",
        tickcolor="rgba(46,58,78,0.6)",
        tickfont=dict(color="#8A94A6", size=11),
    ),
    yaxis=dict(
        gridcolor="rgba(46,58,78,0.5)",
        linecolor="rgba(46,58,78,0.6)",
        tickcolor="rgba(46,58,78,0.6)",
        tickfont=dict(color="#8A94A6", size=11),
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(46,58,78,0.5)",
        font=dict(color="#8A94A6"),
    ),
)

ORANGE_PALETTE = ["#F8BE14","#FBCF4A","#FDDE7E","#C8A000","#A07C00",
                  "#7A5F00","#FFF0B3","#E0B800","#FFE566"]

MULTI_PALETTE  = ["#F8BE14","#8651CA","#94772B","#4E7CFF","#F65164",
                  "#22C55E","#4E7CFF","#FBCF4A","#A07ADA","#4ADE80"]

def _init_theme():
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

def _get_css(is_dark: bool) -> str:
    if is_dark:
        vars_block = """
  --bg-primary:    #1A1F2E;
  --bg-secondary:  #22293A;
  --bg-card:       #22293A;
  --border-color:  #2E3A4E;
  --text-primary:  #F0EEE8;
  --text-muted:    #8A94A6;
  --text-sub:      #5C6680;
  --accent:        #F8BE14;
  --accent-secondary: #8651CA;
  --accent-tertiary:  #94772B;
  --accent-light:  rgba(248,190,20,0.15);
  --accent-border: rgba(248,190,20,0.35);
  --green:         #22C55E;
  --red:           #EF4444;
  --blue:          #4E7CFF;
  --sidebar-bg:    linear-gradient(180deg,#141828 0%,#1A1F2E 100%);
  --shadow:        0 4px 24px rgba(0,0,0,0.5);
  --chart-grid:    #2E3A4E;
  --body-bg:       #1A1F2E;
  --body-text:     #F0EEE8;
"""
    else:
        vars_block = """
  --bg-primary:    #EDEEF5;
  --bg-secondary:  #F5F5FA;
  --bg-card:       #FFFFFF;
  --border-color:  #D8D9E8;
  --text-primary:  #1A1B2E;
  --text-muted:    #5C6680;
  --text-sub:      #8A94A6;
  --accent:        #4E7CFF;
  --accent-secondary: #7033FF;
  --accent-tertiary:  #F65164;
  --accent-light:  rgba(78,124,255,0.12);
  --accent-border: rgba(78,124,255,0.35);
  --green:         #16A34A;
  --red:           #F65164;
  --blue:          #4E7CFF;
  --sidebar-bg:    linear-gradient(180deg,#E8EAF2 0%,#EDEEF5 100%);
  --shadow:        0 4px 12px rgba(26,27,46,0.10);
  --chart-grid:    #D8D9E8;
  --body-bg:       #EDEEF5;
  --body-text:     #1A1B2E;
"""

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

:root {{{vars_block}}}

/* ═══ RESET / BASE ═══════════════════════════════════════ */
*, *::before, *::after {{ box-sizing: border-box; }}

html, body {{
  font-family: 'Inter', 'Manrope', sans-serif !important;
  background-color: var(--body-bg) !important;
  color: var(--body-text) !important;
}}

.stApp,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {{
  background-color: var(--body-bg) !important;
  color: var(--body-text) !important;
  font-family: 'Inter', 'Manrope', sans-serif !important;
}}

.main .block-container {{
  background-color: var(--body-bg) !important;
  padding-top: 1.5rem !important;
  padding-bottom: 2rem !important;
  max-width: 1300px !important;
}}

/* ═══ SIDEBAR ════════════════════════════════════════════ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {{
  background: var(--sidebar-bg) !important;
  border-right: 1px solid var(--border-color) !important;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span:not([data-testid="stPageLink"] span),
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {{
  color: var(--text-sub) !important;
}}

/* ── Sidebar Page Links ───────────────────────────────── */
[data-testid="stSidebarNav"] {{ display: none !important; }}

/* Fixed Next Button Styling */
.next-button-container {{
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 1000;
}}
.st-next-btn a {{
    background: var(--accent) !important;
    color: white !important;
    padding: 12px 24px !important;
    border-radius: 50px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(248,190,20,0.4) !important;
    text-decoration: none !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}
.st-next-btn a:hover {{
    transform: scale(1.08) translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(248,190,20,0.5) !important;
}}

/* Sidebar Toggle Button Visibility Fix */
[data-testid="stHeader"] {{
    background: transparent !important;
    height: 3rem !important;
}}
[data-testid="stHeader"] button {{
    background-color: var(--accent) !important;
    border: none !important;
    border-radius: 50% !important;
    color: white !important;
    margin-left: 10px !important;
    box-shadow: 0 4px 10px rgba(248,190,20,0.3) !important;
    width: 40px !important;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}
[data-testid="stHeader"] button:hover {{
    transform: scale(1.1) !important;
    box-shadow: 0 6px 15px rgba(248,190,20,0.4) !important;
}}

[data-testid="stSidebar"] a[data-testid="stPageLink"] {{
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: 12px !important;
  padding: 10px 14px !important;
  margin-bottom: 6px !important;
  transition: all 0.2s ease !important;
  text-decoration: none !important;
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  width: 100% !important;
}}
[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover {{
  background: var(--bg-secondary) !important;
  border-color: var(--accent) !important;
  transform: translateX(4px) !important;
  box-shadow: var(--shadow) !important;
}}
[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover *,
[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover span,
[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover p {{
  color: var(--accent) !important;
}}
[data-testid="stSidebar"] a[data-testid="stPageLink"][aria-current="page"] {{
  background: linear-gradient(90deg, var(--accent), #FBCF4A) !important;
  border-color: var(--accent) !important;
  box-shadow: 0 4px 15px rgba(248,190,20,0.35) !important;
  transform: none !important;
}}
[data-testid="stSidebar"] a[data-testid="stPageLink"][aria-current="page"] *,
[data-testid="stSidebar"] a[data-testid="stPageLink"][aria-current="page"] span,
[data-testid="stSidebar"] a[data-testid="stPageLink"][aria-current="page"] p {{
  color: #FFFFFF !important;
  font-weight: 700 !important;
}}
[data-testid="stSidebar"] a[data-testid="stPageLink"] span,
[data-testid="stSidebar"] a[data-testid="stPageLink"] p {{
  color: var(--text-primary) !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
}}

/* ── Sidebar Buttons ─────────────────────────────────── */
[data-testid="stSidebar"] .stButton > button {{
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: 10px !important;
  color: var(--text-primary) !important;
  font-family: 'Inter', 'Manrope', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  padding: 8px 14px !important;
  transition: all 0.2s ease !important;
  width: 100%;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
  border-color: var(--accent) !important;
  color: var(--accent) !important;
  background: var(--bg-secondary) !important;
}}

/* ── Selectbox ───────────────────────────────────────── */
[data-baseweb="select"] > div {{
  background: var(--bg-card) !important;
  border-color: var(--border-color) !important;
  color: var(--text-primary) !important;
}}
[data-baseweb="popover"] ul,
[data-baseweb="menu"] {{ background: var(--bg-card) !important; }}
[data-baseweb="menu"] li {{ color: var(--text-primary) !important; }}
[data-baseweb="menu"] li:hover {{ background: var(--bg-secondary) !important; }}
[data-baseweb="select"] svg {{ fill: var(--text-muted) !important; }}

/* ── Slider ─────────────────────────────────────────── */
[data-testid="stSlider"] [role="slider"] {{
  background: var(--accent) !important;
}}

/* ═══ HEADER ═════════════════════════════════════════════ */
.dash-header {{
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px 32px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow);
}}
.dash-header::before {{
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent), #FBCF4A, #8651CA);
}}
.dash-header h1 {{
  font-size: clamp(1.3rem, 4vw, 2rem) !important;
  font-weight: 800 !important;
  color: var(--text-primary) !important;
  margin: 0 0 8px 0 !important;
  letter-spacing: -0.5px !important;
  line-height: 1.2 !important;
}}
.dash-header p {{
  color: var(--text-muted) !important;
  font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
  margin: 0 !important;
}}
.dash-badge {{
  display: inline-block;
  background: var(--accent-light);
  border: 1px solid var(--accent-border);
  color: var(--accent);
  font-size: 0.68rem; font-weight: 700;
  padding: 3px 10px; border-radius: 20px;
  letter-spacing: 0.8px; text-transform: uppercase;
  margin-bottom: 10px;
}}

/* ═══ KPI CARDS ══════════════════════════════════════════ */
.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}}
.kpi-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 18px 16px 14px;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
  box-shadow: var(--shadow);
}}
.kpi-card:hover {{
  transform: translateY(-3px);
  border-color: var(--accent);
  box-shadow: 0 8px 32px rgba(248,190,20,0.18);
}}
.kpi-card::after {{
  content: '';
  position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent), #FBCF4A);
  transform: scaleX(0); transform-origin: left;
  transition: transform 0.3s;
}}
.kpi-card:hover::after {{ transform: scaleX(1); }}
.kpi-icon  {{ font-size: 1.4rem; margin-bottom: 8px; }}
.kpi-label {{ color: var(--text-muted); font-size: 0.7rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 5px; }}
.kpi-value {{ color: var(--text-primary); font-size: clamp(1.2rem, 3vw, 1.7rem); font-weight: 800; line-height: 1; }}
.kpi-sub   {{ color: var(--text-sub); font-size: 0.75rem; margin-top: 5px; }}
.kpi-delta-pos {{ color: var(--green); font-size: 0.74rem; font-weight: 600; }}
.kpi-delta-neg {{ color: var(--red);   font-size: 0.74rem; font-weight: 600; }}

/* ═══ SECTION TITLE ══════════════════════════════════════ */
.section-title {{
  color: var(--text-primary);
  font-size: 1rem; font-weight: 700;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 18px;
  display: flex; align-items: center; gap: 8px;
}}
.section-title .dot {{
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--accent); display: inline-block; flex-shrink: 0;
}}

/* ═══ CHART CARD ═════════════════════════════════════════ */
.chart-card {{
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow);
}}

/* ═══ MISC ═══════════════════════════════════════════════ */
.dash-divider {{ border: none; border-top: 1px solid var(--border-color); margin: 20px 0; }}

.pill {{ display: inline-block; border-radius: 20px; padding: 2px 10px; font-size: 0.72rem; font-weight: 600; }}
.pill-green {{ background: rgba(34,197,94,0.15);  color: var(--green); border: 1px solid rgba(34,197,94,0.3); }}
.pill-red   {{ background: rgba(239,68,68,0.15);  color: var(--red);   border: 1px solid rgba(239,68,68,0.3); }}
.pill-amber {{ background: var(--accent-light);   color: var(--accent); border: 1px solid var(--accent-border); }}
.pill-blue  {{ background: rgba(56,189,248,0.15); color: var(--blue);  border: 1px solid rgba(56,189,248,0.3); }}

.pred-result {{
  background: linear-gradient(135deg, var(--bg-secondary), var(--bg-primary));
  border: 1px solid var(--accent);
  border-radius: 16px; padding: 28px;
  text-align: center; margin-top: 20px;
  box-shadow: var(--shadow);
}}
.pred-result .pred-label {{ color: var(--text-muted); font-size: 0.85rem; margin-bottom: 8px; }}
.pred-result .pred-value {{ color: var(--accent); font-size: 2rem; font-weight: 700; }}

.brand-panel {{
  background: linear-gradient(135deg, var(--bg-secondary), var(--bg-primary));
  border: 1px solid var(--border-color);
  border-radius: 14px; padding: 18px 20px 12px;
  margin-bottom: 16px; box-shadow: var(--shadow);
}}

.footer-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px; text-align: center;
}}
.footer-item {{
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px; padding: 18px;
  transition: border-color 0.2s, transform 0.2s;
}}
.footer-item:hover {{ border-color: var(--accent); transform: translateY(-2px); }}
.footer-item .fi-icon {{ font-size: 1.5rem; }}
.footer-item .fi-title {{ color: var(--text-primary); font-weight: 700; margin: 6px 0 4px; font-size: 0.9rem; }}
.footer-item .fi-desc  {{ color: var(--text-muted); font-size: 0.78rem; }}

/* ═══ STREAMLIT CHROME ═══════════════════════════════════ */
#MainMenu, footer {{ visibility: hidden; }}

/* ═══ NATIVE STREAMLIT METRIC ════════════════════════════ */
[data-testid="metric-container"] {{
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: 12px !important;
  padding: 16px !important;
}}
[data-testid="metric-container"] label {{ color: var(--text-muted) !important; }}
[data-testid="stMetricValue"] {{ color: var(--text-primary) !important; }}

/* ═══ RESPONSIVE ═════════════════════════════════════════ */
@media (max-width: 768px) {{
  .main .block-container {{
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
    max-width: 100% !important;
  }}
  .dash-header {{ padding: 16px; border-radius: 12px; }}
  .kpi-grid {{ grid-template-columns: repeat(2, 1fr) !important; gap: 10px; }}
  .kpi-value {{ font-size: 1.25rem !important; }}
  .kpi-card {{ padding: 14px 12px; }}
  .footer-grid {{ grid-template-columns: 1fr !important; }}
  [data-testid="column"] {{
    width: 100% !important;
    flex: 1 1 100% !important;
    min-width: 100% !important;
  }}
}}
@media (max-width: 480px) {{
  .kpi-grid {{ grid-template-columns: 1fr !important; }}
}}
@media (min-width: 769px) and (max-width: 1024px) {{
  .kpi-grid {{ grid-template-columns: repeat(3, 1fr) !important; }}
  .footer-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
}}
</style>
"""

def inject_css():
    _init_theme()
    is_dark = st.session_state.get("dark_mode", True)
    st.markdown(_get_css(is_dark), unsafe_allow_html=True)

def sidebar_brand():
    st.markdown(f"""
    <div style="padding:14px 0 14px">
      <div style="font-size:1.3rem;font-weight:900;color:var(--text-primary,#F0EEE8);
                  letter-spacing:-0.5px;margin-bottom:4px;">\U0001F6D2 EcomIQ</div>
      <div style="color:var(--text-muted,#8A94A6);font-size:0.72rem;margin-bottom:14px;">
        Sales &amp; ML Analytics Platform
      </div>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
        {MEESHO_LOGO_SVG}
        {AMAZON_LOGO_SVG}
      </div>
    </div>
    <hr style="border-color:var(--border-color,#2E3A4E);margin-bottom:14px">
    """, unsafe_allow_html=True)

def sidebar_nav():
    """Centralized sidebar navigation with dark/light mode toggle."""
    _init_theme()

    with st.sidebar:
        sidebar_brand()

        is_dark = st.session_state.get("dark_mode", True)
        toggle_label = "\u2600\uFE0F Switch to Light Mode" if is_dark else "\U0001F319 Switch to Dark Mode"

        if st.button(toggle_label, key="theme_toggle_btn", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

        st.markdown('<hr style="border-color:var(--border-color,#2E3A4E);margin:12px 0">', unsafe_allow_html=True)

        st.markdown(
            '<div style="color:var(--text-muted,#8A94A6);font-size:0.7rem;font-weight:700;'
            'text-transform:uppercase;letter-spacing:1.5px;margin:0 0 8px 2px;">Navigation</div>',
            unsafe_allow_html=True
        )

        st.page_link("Home.py",               label="\U0001F3E0 Home Dashboard")
        st.page_link("pages/1_Meesho.py",     label="\U0001F6CD\uFE0F Meesho Stats")
        st.page_link("pages/2_Amazon.py",     label="\U0001F4E6 Amazon Stats")
        st.page_link("pages/3_ML_Models.py",  label="\U0001F9BE ML Models")
        st.page_link("pages/4_Customer.py",   label="\U0001F4CA Customer Trends")
        st.page_link("pages/5_Prediction.py", label="\U0001F52E Live Predictor")

        st.markdown('<hr style="border-color:var(--border-color,#2E3A4E);margin:14px 0 8px">', unsafe_allow_html=True)
        st.markdown(
            '<div style="color:var(--text-muted,#8A94A6);font-size:0.65rem;text-align:center;">'
            'BSc Data Science · 2025–26</div>',
            unsafe_allow_html=True
        )

    nav_order = [
        ("Home.py", "\U0001F3E0 Home"),
        ("pages/1_Meesho.py", "\U0001F6CD\uFE0F Meesho Stats"),
        ("pages/2_Amazon.py", "\U0001F4E6 Amazon Stats"),
        ("pages/3_ML_Models.py", "\U0001F9BE ML Models"),
        ("pages/4_Customer.py", "\U0001F4CA Customer Trends"),
        ("pages/5_Prediction.py", "\U0001F52E Live Predictor")
    ]

    current_page = "Home.py"
    try:
        import os
        import inspect
        caller_path = inspect.stack()[1].filename
        current_page_file = os.path.basename(caller_path)

        for i, (f, label) in enumerate(nav_order):
            if os.path.basename(f) == current_page_file:
                next_idx = (i + 1) % len(nav_order)
                next_f, next_label = nav_order[next_idx]

                st.markdown('<div class="next-button-container st-next-btn">', unsafe_allow_html=True)
                st.page_link(next_f, label=f"Next: {next_label} →")
                st.markdown('</div>', unsafe_allow_html=True)
                break
    except Exception as e:
        pass

def header(title: str, subtitle: str, badge: str = "", logo: str = ""):
    badge_html = f'<div class="dash-badge">{badge}</div>' if badge else ""
    logo_map = {"meesho": MEESHO_LOGO_SVG, "amazon": AMAZON_LOGO_SVG}
    logo_html = ""
    if logo and logo in logo_map:
        logo_html = f'<div style="margin-bottom:12px">{logo_map[logo]}</div>'
    st.markdown(f"""<div class="dash-header">
{logo_html}{badge_html}
<h1>{title}</h1>
<p>{subtitle}</p>
</div>""", unsafe_allow_html=True)

def kpi_card(icon: str, label: str, value: str, sub: str = "", delta: str = "", delta_pos: bool = True):
    delta_class = "kpi-delta-pos" if delta_pos else "kpi-delta-neg"
    delta_html  = f'<div class="{delta_class}">{delta}</div>' if delta else ""
    sub_html    = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return f"""<div class="kpi-card">
    <div class="kpi-icon">{icon}</div>
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}</div>
    {sub_html}{delta_html}
</div>"""

def kpi_row(cards: list):
    st.markdown('<div class="kpi-grid">' + "".join(cards) + '</div>', unsafe_allow_html=True)

def section(title: str):
    st.markdown(
        f'<div class="section-title"><span class="dot"></span>{title}</div>',
        unsafe_allow_html=True
    )

def chart_card(fig, title: str = ""):
    title_html = (
        f'<div style="color:var(--text-sub);font-size:0.78rem;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:0.8px;margin-bottom:12px;">{title}</div>'
        if title else ""
    )
    st.markdown(f'<div class="chart-card">{title_html}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", config={"displayModeBar": False})
