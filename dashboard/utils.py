import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────────────────────
# INLINE SVG LOGOS  – official brand marks
# ─────────────────────────────────────────────────────────────

# Meesho logo (official pink‑magenta wordmark colours)
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

# Amazon logo (official orange smile wordmark)
AMAZON_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 40" width="110" height="32">
  <rect width="140" height="40" rx="6" fill="#131921"/>
  <text x="12" y="22" font-family="Arial,sans-serif" font-weight="900"
        font-size="16" fill="#ffffff" letter-spacing="-0.3">amazon</text>
  <!-- smile arrow -->
  <path d="M12 30 Q50 38 88 30" stroke="#FF9900" stroke-width="2.5"
        fill="none" stroke-linecap="round"/>
  <polygon points="84,27 90,30 84,33" fill="#FF9900"/>
</svg>"""

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS  – CSS-variable driven, supports dark & light modes
#              + full mobile responsiveness
# ─────────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════════════════════════
   CSS VARIABLES  – dark theme (Streamlit default dark)
   ═══════════════════════════════════════════════════════════ */
:root {
  --bg-primary:    #0F172A;
  --bg-secondary:  #1E293B;
  --bg-card:       #1E293B;
  --border-color:  #1E3A5F;
  --text-primary:  #F1F5F9;
  --text-muted:    #64748B;
  --text-sub:      #94A3B8;
  --accent:        #F97316;
  --accent-light:  rgba(249,115,22,0.15);
  --accent-border: rgba(249,115,22,0.35);
  --green:         #22C55E;
  --red:           #EF4444;
  --blue:          #38BDF8;
  --sidebar-bg:    linear-gradient(180deg,#0A1628 0%,#0F172A 100%);
  --shadow:        0 4px 24px rgba(0,0,0,0.4);
  --chart-grid:    #1E3A5F;
}

/* ── Light theme overrides ──────────────────────────────── */
[data-theme="light"],
.stApp[data-theme="light"],
.stApp.light {
  --bg-primary:    #F8FAFC;
  --bg-secondary:  #F1F5F9;
  --bg-card:       #FFFFFF;
  --border-color:  #E2E8F0;
  --text-primary:  #0F172A;
  --text-muted:    #64748B;
  --text-sub:      #475569;
  --accent:        #EA580C;
  --accent-light:  rgba(234,88,12,0.10);
  --accent-border: rgba(234,88,12,0.30);
  --sidebar-bg:    linear-gradient(180deg,#F1F5F9 0%,#E2E8F0 100%);
  --shadow:        0 4px 12px rgba(0,0,0,0.05);
  --chart-grid:    #E2E8F0;
}

/* Base override to ensure variables are applied */
.stApp {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Base ────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
  font-family: 'DM Sans', sans-serif !important;
  background-color: var(--bg-primary) !important;
}

/* ── Sidebar ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--sidebar-bg) !important;
  border-right: 1px solid var(--border-color);
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: var(--text-sub) !important; font-size: 0.82rem; }

/* ── Sidebar Buttons ──────────────────────────────────────── */
[data-testid="stSidebar"] a[data-testid="stPageLink"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin-bottom: 8px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    text-decoration: none !important;
    color: var(--text-primary) !important;
    display: flex !important;
    align-items: center !important;
}

[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover {
    background: var(--bg-secondary) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: translateX(6px);
    box-shadow: var(--shadow);
}

[data-testid="stSidebar"] a[data-testid="stPageLink"][aria-current="page"] {
    background: linear-gradient(90deg, var(--accent), #FB923C) !important;
    border-color: var(--accent) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(249,115,22,0.4);
}

[data-testid="stSidebar"] a[data-testid="stPageLink"] span {
    color: inherit !important;
    font-size: 0.9rem !important;
    font-weight: 500;
}

[data-testid="stSidebar"] a[data-testid="stPageLink"][aria-current="page"] span {
    color: #FFFFFF !important;
}

/* ── Top header bar ──────────────────────────────────────── */
.dash-header {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px 32px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow);
}
.dash-header h1 {
  font-size: clamp(1.4rem, 5vw, 2.2rem) !important;
  font-weight: 800 !important;
  color: var(--text-primary) !important;
  margin: 0 0 8px 0 !important;
  letter-spacing: -1px !important;
  line-height: 1.2 !important;
}
.dash-header p {
  color: var(--text-muted) !important;
  font-size: clamp(0.85rem, 2vw, 1rem) !important;
  margin: 0 !important;
  max-width: 800px;
}
.dash-badge {
  display: inline-block;
  background: var(--accent-light);
  border: 1px solid var(--accent-border);
  color: var(--accent);
  font-size: 0.72rem; font-weight: 600;
  padding: 3px 10px; border-radius: 20px;
  letter-spacing: 0.5px; text-transform: uppercase;
  margin-bottom: 10px;
}

/* ── Logo badge in header ────────────────────────────────── */
.platform-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}
.platform-logo svg { border-radius: 6px; }

/* ── KPI Cards ───────────────────────────────────────────── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 14px;
  margin-bottom: 28px;
}
.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 18px 16px 14px;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
  box-shadow: var(--shadow);
}
.kpi-card:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
  box-shadow: 0 8px 32px rgba(249,115,22,0.15);
}
.kpi-card::after {
  content: '';
  position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent), #FB923C);
  transform: scaleX(0); transform-origin: left;
  transition: transform 0.3s;
}
.kpi-card:hover::after { transform: scaleX(1); }
.kpi-icon  { font-size: 1.4rem; margin-bottom: 8px; }
.kpi-label { color: var(--text-muted); font-size: 0.73rem; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 5px; }
.kpi-value { color: var(--text-primary); font-size: clamp(1.3rem, 3vw, 1.7rem); font-weight: 700; line-height: 1; }
.kpi-sub   { color: var(--text-sub); font-size: 0.76rem; margin-top: 5px; }
.kpi-delta-pos { color: var(--green); font-size: 0.76rem; font-weight: 600; }
.kpi-delta-neg { color: var(--red);   font-size: 0.76rem; font-weight: 600; }

/* ── Section titles ──────────────────────────────────────── */
.section-title {
  color: var(--text-primary);
  font-size: 1.05rem; font-weight: 600;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 18px;
  display: flex; align-items: center; gap: 8px;
}
.section-title .dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--accent); display: inline-block;
}

/* ── Chart card ──────────────────────────────────────────── */
.chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow);
}
.chart-card-title {
  color: var(--text-sub);
  font-size: 0.8rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.8px;
  margin-bottom: 14px;
}

/* ── Data table ──────────────────────────────────────────── */
.dataframe { border-radius: 10px !important; overflow: hidden !important; }

/* ── Divider ─────────────────────────────────────────────── */
.dash-divider { border: none; border-top: 1px solid var(--border-color); margin: 24px 0; }

/* ── Pill tag ────────────────────────────────────────────── */
.pill {
  display: inline-block; border-radius: 20px;
  padding: 2px 10px; font-size: 0.72rem; font-weight: 600;
}
.pill-green { background: rgba(34,197,94,0.15);  color: var(--green); border: 1px solid rgba(34,197,94,0.3); }
.pill-red   { background: rgba(239,68,68,0.15);  color: var(--red);   border: 1px solid rgba(239,68,68,0.3); }
.pill-amber { background: var(--accent-light);   color: var(--accent); border: 1px solid var(--accent-border); }
.pill-blue  { background: rgba(56,189,248,0.15); color: var(--blue);  border: 1px solid rgba(56,189,248,0.3); }

/* ── Prediction card ─────────────────────────────────────── */
.pred-result {
  background: linear-gradient(135deg, var(--bg-secondary), var(--bg-primary));
  border: 1px solid var(--accent);
  border-radius: 16px;
  padding: 28px;
  text-align: center;
  margin-top: 20px;
  box-shadow: var(--shadow);
}
.pred-result .pred-label { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 8px; }
.pred-result .pred-value { color: var(--accent); font-size: 2rem; font-weight: 700; }

/* ── Brand panels (Meesho / Amazon blocks) ───────────────── */
.brand-panel {
  background: linear-gradient(135deg, var(--bg-secondary), var(--bg-primary));
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 18px 20px 12px;
  margin-bottom: 16px;
  box-shadow: var(--shadow);
}

/* ── Footer grid ─────────────────────────────────────────── */
.footer-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  text-align: center;
}
.footer-item {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 18px;
  transition: border-color 0.2s;
}
.footer-item:hover { border-color: var(--accent); }
.footer-item .fi-icon { font-size: 1.5rem; }
.footer-item .fi-title { color: var(--text-primary); font-weight: 600; margin: 6px 0 4px; font-size: 0.95rem; }
.footer-item .fi-desc  { color: var(--text-muted); font-size: 0.8rem; }

/* ── Hide Streamlit chrome ───────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
  padding-top: 1.5rem !important;
  padding-bottom: 1rem !important;
  max-width: 1200px !important;
}

/* ══════════════════════════════════════════════════════════
   MOBILE RESPONSIVE  (≤ 768 px)
   ══════════════════════════════════════════════════════════ */
@media (max-width: 768px) {
  .block-container {
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
    max-width: 100% !important;
  }

  /* Header */
  .dash-header { padding: 18px 18px; border-radius: 12px; }
  .dash-header h1 { font-size: 1.35rem; }
  .dash-header p  { font-size: 0.8rem; }

  /* KPI grid – 1 column on very small mobile */
  .kpi-grid {
    grid-template-columns: 1fr !important;
    gap: 12px;
  }
  @media (min-width: 480px) {
    .kpi-grid { grid-template-columns: repeat(2, 1fr) !important; }
  }
  .kpi-value { font-size: 1.5rem !important; }
  .kpi-card  { padding: 16px 14px; }

  /* Footer grid – 1 column on mobile */
  .footer-grid { grid-template-columns: 1fr !important; }

  /* Charts – ensure full width */
  .js-plotly-plot, .plotly, .plot-container { width: 100% !important; }

  /* Sidebar brand header */
  [data-testid="stSidebar"] { min-width: 260px !important; }

  /* Section title */
  .section-title { font-size: 0.95rem; }

  /* Force columns to stack on mobile */
  [data-testid="column"], [data-testid="stVerticalBlock"] > [style*="flex-direction: row"] > [data-testid="stColumn"] {
    width: 100% !important;
    flex: 1 1 100% !important;
    min-width: 100% !important;
    margin-bottom: 1rem;
  }
}

/* ── Tablet (769–1024px) ─────────────────────────────────── */
@media (min-width: 769px) and (max-width: 1024px) {
  .kpi-grid { grid-template-columns: repeat(3, 1fr) !important; }
  .footer-grid { grid-template-columns: repeat(2, 1fr) !important; }
}
</style>
"""

# ─────────────────────────────────────────────────────────────
# PLOTLY DEFAULT LAYOUT  – uses transparent bg; adapts to themes via neutral colors
# ─────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#64748B", size=12),
    margin=dict(l=10, r=10, t=32, b=10),
    xaxis=dict(
        gridcolor="rgba(100, 116, 139, 0.1)", 
        linecolor="rgba(100, 116, 139, 0.2)", 
        tickcolor="rgba(100, 116, 139, 0.2)",
        tickfont=dict(color="#94A3B8", size=11),
    ),
    yaxis=dict(
        gridcolor="rgba(100, 116, 139, 0.1)", 
        linecolor="rgba(100, 116, 139, 0.2)", 
        tickcolor="rgba(100, 116, 139, 0.2)",
        tickfont=dict(color="#94A3B8", size=11),
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)", 
        bordercolor="rgba(100, 116, 139, 0.2)",
        font=dict(color="#64748B"),
    ),
)

ORANGE_PALETTE = ["#F97316","#FB923C","#FDBA74","#FED7AA","#FFF7ED",
                  "#EA580C","#C2410C","#9A3412","#7C2D12"]

MULTI_PALETTE  = ["#F97316","#38BDF8","#A78BFA","#34D399","#F472B6",
                  "#FBBF24","#60A5FA","#4ADE80","#FB7185","#A3E635"]


def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def sidebar_brand():
    """Render the EcomIQ brand block with Meesho + Amazon logos in sidebar."""
    st.markdown(f"""
    <div style="padding:14px 0 18px">
      <div style="font-size:1.25rem;font-weight:800;color:var(--text-primary,#F1F5F9);
                  letter-spacing:-0.5px;margin-bottom:4px;">🛒 EcomIQ</div>
      <div style="color:var(--text-muted,#64748B);font-size:0.75rem;margin-bottom:14px;">
        Sales &amp; ML Analytics Platform
      </div>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
        {MEESHO_LOGO_SVG}
        {AMAZON_LOGO_SVG}
      </div>
    </div>
    <hr style="border-color:#1E3A5F;margin-bottom:18px">
    """, unsafe_allow_html=True)


def sidebar_nav():
    """Centralized sidebar navigation used across all pages.
    Includes brand, then quick links to each page.
    """
    with st.sidebar:
        sidebar_brand()
        
        # Section header for Navigation
        st.markdown('<div style="color:var(--text-muted);font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;margin:10px 0 12px 10px;">Navigation</div>', unsafe_allow_html=True)
        
        st.page_link("Home.py",               label="🏠 Home Dashboard")
        st.page_link("pages/1_Meesho.py",     label="🛍️ Meesho Stats")
        st.page_link("pages/2_Amazon.py",     label="📦 Amazon Stats")
        st.page_link("pages/3_ML_Models.py",  label="🦾 ML Models")
        st.page_link("pages/4_Customer.py",   label="📊 Trends")
        st.page_link("pages/5_Prediction.py", label="🔮 Predictor")
        
        st.markdown('<hr style="border-color:var(--border-color);margin:20px 0 12px">', unsafe_allow_html=True)
        
        # Add a Standalone Home Button at the bottom for quick access
        st.sidebar.markdown('<br>', unsafe_allow_html=True)
        if st.sidebar.button("🏠 Back to Home", use_container_width=True):
             st.switch_page("Home.py")
             
        st.markdown('<div style="color:var(--text-muted);font-size:0.7rem;text-align:center;margin-top:20px;">Academic Year 2025–26</div>', unsafe_allow_html=True)


def header(title: str, subtitle: str, badge: str = "", logo: str = ""):
    """
    logo: 'meesho' | 'amazon' | '' for no platform logo
    """
    badge_html = f'<div class="dash-badge">{badge}</div>' if badge else ""
    logo_map = {"meesho": MEESHO_LOGO_SVG, "amazon": AMAZON_LOGO_SVG}
    logo_html = ""
    if logo and logo in logo_map:
        logo_html = f'<div class="platform-logo">{logo_map[logo]}</div>'
    
    # Use st.html for cleaner rendering if available, fallback to st.markdown
    html_content = f"""<div class="dash-header">
{logo_html}
{badge_html}
<h1>{title}</h1>
<p>{subtitle}</p>
</div>"""
    st.markdown(html_content, unsafe_allow_html=True)


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
    st.markdown(f'<div class="section-title"><span class="dot"></span>{title}</div>',
                unsafe_allow_html=True)


def chart_card(fig, title: str = ""):
    title_html = f'<div class="chart-card-title">{title}</div>' if title else ""
    st.markdown(f'<div class="chart-card">{title_html}</div>', unsafe_allow_html=True)
    # Using 'streamlit' theme for better auto-adaptation
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", config={"displayModeBar": False})
