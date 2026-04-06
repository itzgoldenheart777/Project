import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from utils import *

st.set_page_config(
    page_title="E-Commerce Analytics | Home",
    page_icon="\U0001F6D2",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

sidebar_nav()

header(
    "E-Commerce Sales & Customer Analytics",
    "Machine Learning powered insights from Meesho & Amazon datasets · BSc Data Science",
    badge="Dashboard · 2025–26"
)

@st.cache_data
def load_all():
    m = pd.read_csv("data/meesho Orders Aug.csv")
    m.columns = m.columns.str.strip()
    m.rename(columns={"Reason for Credit Entry": "Order_Status",
                       "Supplier Listed Price (Incl. GST + Commission)": "Price"}, inplace=True)

    a = pd.read_csv("data/Amazon Sale Report.csv", low_memory=False)
    a.columns = a.columns.str.strip()
    a["Date"]   = pd.to_datetime(a["Date"], errors="coerce", dayfirst=False)
    a["Month"]  = a["Date"].dt.month
    a["Amount"] = pd.to_numeric(a["Amount"], errors="coerce")
    a["Qty"]    = pd.to_numeric(a["Qty"], errors="coerce")
    return m, a

meesho, amazon = load_all()

m_total   = len(meesho)
m_del     = (meesho["Order_Status"] == "DELIVERED").sum()
m_rev     = meesho["Price"].sum()
m_cancel  = (meesho["Order_Status"] == "CANCELLED").sum()

a_total   = len(amazon)
a_del     = amazon["Status"].str.contains("Delivered", na=False).sum()
a_rev     = amazon["Amount"].sum()
a_cancel  = (amazon["Status"] == "Cancelled").sum()

section("Platform Overview")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="brand-panel">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">
            {MEESHO_LOGO_SVG}
            <div style="color:var(--text-muted,#8A94A6);font-size:0.75rem">Orders Aug Dataset</div>
        </div>
    </div>""", unsafe_allow_html=True)
    kpi_row([
        kpi_card("\U0001F4CB","Total Orders", f"{m_total:,}"),
        kpi_card("\u2705","Delivered", f"{m_del:,}", delta=f"{m_del/m_total*100:.1f}%", delta_pos=True),
        kpi_card("\u274C","Cancelled",  f"{m_cancel:,}", delta=f"{m_cancel/m_total*100:.1f}%", delta_pos=False),
        kpi_card("\U0001F4B0","Revenue",    f"₹{m_rev/1e3:.1f}K"),
    ])

with col2:
    st.markdown(f"""
    <div class="brand-panel">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">
            {AMAZON_LOGO_SVG}
            <div style="color:var(--text-muted,#8A94A6);font-size:0.75rem">Sale Report Dataset</div>
        </div>
    </div>""", unsafe_allow_html=True)
    kpi_row([
        kpi_card("\U0001F4CB","Total Orders", f"{a_total:,}"),
        kpi_card("\u2705","Delivered",    f"{a_del:,}",    delta=f"{a_del/a_total*100:.1f}%", delta_pos=True),
        kpi_card("\u274C","Cancelled",    f"{a_cancel:,}", delta=f"{a_cancel/a_total*100:.1f}%", delta_pos=False),
        kpi_card("\U0001F4B0","Revenue",      f"₹{a_rev/1e7:.2f}Cr"),
    ])

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

section("Order Status Comparison")
c1, c2 = st.columns(2)

with c1:
    m_status = meesho["Order_Status"].value_counts().reset_index()
    m_status.columns = ["Status","Count"]
    color_map = {"DELIVERED":"#22C55E","CANCELLED":"#EF4444","RTO_COMPLETE":"#F8BE14","RTO_LOCKED":"#8651CA"}
    fig = px.pie(m_status, names="Status", values="Count",
                 color="Status", color_discrete_map=color_map,
                 hole=0.6)
    fig.update_traces(textposition="outside", textfont_size=11,
                      marker=dict(line=dict(color="#141828", width=2)))
    fig.update_layout(**PLOTLY_LAYOUT, title_text="Meesho Order Status",
                      title_font=dict(color="#8A94A6", size=13),
                      showlegend=True)
    fig.add_annotation(text=f"<b>{m_total}</b><br><span style='font-size:10px'>orders</span>",
                       showarrow=False, font=dict(size=16, color="#F0EEE8"),
                       x=0.5, y=0.5)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", config={"displayModeBar": False})

with c2:
    top_statuses = amazon["Status"].value_counts().head(6).reset_index()
    top_statuses.columns = ["Status","Count"]
    a_colors = ["#22C55E","#4E7CFF","#EF4444","#F8BE14","#8651CA","#F8BE14"]
    fig2 = px.pie(top_statuses, names="Status", values="Count",
                  color_discrete_sequence=a_colors, hole=0.6)
    fig2.update_traces(textposition="outside", textfont_size=11,
                       marker=dict(line=dict(color="#141828", width=2)))
    fig2.update_layout(**PLOTLY_LAYOUT, title_text="Amazon Order Status",
                       title_font=dict(color="#8A94A6", size=13))
    fig2.add_annotation(text=f"<b>{a_total:,}</b><br><span style='font-size:9px'>orders</span>",
                        showarrow=False, font=dict(size=16, color="#F0EEE8"),
                        x=0.5, y=0.5)
    st.plotly_chart(fig2, use_container_width=True, theme="streamlit", config={"displayModeBar": False})

section("Amazon Monthly Revenue Trend")
monthly = amazon.groupby("Month")["Amount"].sum().reset_index()
monthly.columns = ["Month","Revenue"]
month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
               7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
monthly["Month_Name"] = monthly["Month"].map(month_names)
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=monthly["Month_Name"], y=monthly["Revenue"],
    mode="lines+markers",
    line=dict(color="#F8BE14", width=3, shape="spline"),
    marker=dict(size=8, color="#F8BE14", line=dict(color="#141828", width=2)),
    fill="tozeroy",
    fillcolor="rgba(248,190,20,0.08)",
    hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
))
fig3.update_layout(**PLOTLY_LAYOUT, height=260,
                   yaxis_tickprefix="₹", yaxis_tickformat=".2s")
st.plotly_chart(fig3, use_container_width=True, theme="streamlit", config={"displayModeBar": False})

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="footer-grid">
    <div class="footer-item">
        <div class="fi-icon">\U0001F916</div>
        <div class="fi-title">ML Classification</div>
        <div class="fi-desc">Logistic Regression, Decision Tree &amp; Random Forest trained on order data</div>
    </div>
    <div class="footer-item">
        <div class="fi-icon">\U0001F4CA</div>
        <div class="fi-title">Multi-Source Data</div>
        <div class="fi-desc">Amazon, Meesho + Google Forms survey — 130K+ records analysed</div>
    </div>
    <div class="footer-item">
        <div class="fi-icon">\U0001F52E</div>
        <div class="fi-title">Live Prediction</div>
        <div class="fi-desc">Enter order details and get instant delivery outcome prediction</div>
    </div>
</div>
""", unsafe_allow_html=True)
