import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import *

st.set_page_config(page_title="Meesho Analytics", page_icon="🛍️", layout="wide")
inject_css()

sidebar_nav()

header("Meesho Sales Analytics", "Order performance, logistics & product intelligence · Aug 2022", badge="Meesho Platform", logo="meesho")


# ── Data ─────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv("data/meesho Orders Aug.csv")
    df.columns = df.columns.str.strip()
    df.rename(columns={
        "Reason for Credit Entry": "Order_Status",
        "Supplier Listed Price (Incl. GST + Commission)": "Price",
        "Supplier Discounted Price (Incl GST and Commision)": "Disc_Price"
    }, inplace=True)
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Order_Value"] = df["Price"] * df["Quantity"]
    return df

df = load()
total  = len(df)
deliv  = (df["Order_Status"] == "DELIVERED").sum()
cancel = (df["Order_Status"] == "CANCELLED").sum()
rto    = df["Order_Status"].str.startswith("RTO", na=False).sum()
rev    = df["Order_Value"].sum()
avg_price = df["Price"].mean()

# ── Sidebar filters ───────────────────────────────────────────
with st.sidebar:
    st.markdown('<hr style="border-color:#1E3A5F;margin:16px 0 12px">', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748B;font-size:0.72rem;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">Filters</div>', unsafe_allow_html=True)
    status_opts = ["All"] + sorted(df["Order_Status"].dropna().unique().tolist())
    sel_status  = st.selectbox("Order Status", status_opts)
    state_opts  = ["All"] + sorted(df["Customer State"].dropna().unique().tolist())
    sel_state   = st.selectbox("State", state_opts)

fdf = df.copy()
if sel_status != "All": fdf = fdf[fdf["Order_Status"] == sel_status]
if sel_state  != "All": fdf = fdf[fdf["Customer State"] == sel_state]

# ── KPIs ─────────────────────────────────────────────────────
kpi_row([
    kpi_card("📋", "Total Orders",    f"{total:,}"),
    kpi_card("✅", "Delivered",       f"{deliv:,}",  delta=f"{deliv/total*100:.1f}%",  delta_pos=True),
    kpi_card("❌", "Cancelled",       f"{cancel:,}", delta=f"{cancel/total*100:.1f}%", delta_pos=False),
    kpi_card("🔄", "RTO",             f"{rto:,}",    delta=f"{rto/total*100:.1f}%",    delta_pos=False),
    kpi_card("💰", "Total Revenue",   f"₹{rev:,.0f}"),
    kpi_card("🏷️", "Avg Price",      f"₹{avg_price:.0f}"),
])

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── Row 1: Status donut + State bar ──────────────────────────
section("Order Distribution")
c1, c2 = st.columns([1, 1.6])

with c1:
    status_counts = fdf["Order_Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    cmap = {"DELIVERED":"#22C55E","CANCELLED":"#EF4444","RTO_COMPLETE":"#F97316","RTO_LOCKED":"#F59E0B"}
    fig = px.pie(status_counts, names="Status", values="Count",
                 color="Status", color_discrete_map=cmap, hole=0.6)
    fig.update_traces(textposition="outside", textfont_size=10,
                      marker=dict(line=dict(color="#0F172A", width=2)))
    layout = PLOTLY_LAYOUT.copy()
    layout.update({"height": 320, "showlegend": True,
                   "legend": dict(orientation="h", y=-0.15)})
    fig.update_layout(**layout)
    fig.add_annotation(text=f"<b>{len(fdf)}</b><br>orders", showarrow=False,
                       font=dict(size=15, color="#F1F5F9"), x=0.5, y=0.5)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    top_states = fdf["Customer State"].value_counts().head(12).reset_index()
    top_states.columns = ["State","Orders"]
    fig2 = go.Figure(go.Bar(
        x=top_states["Orders"], y=top_states["State"],
        orientation="h",
        marker=dict(
            color=top_states["Orders"],
            colorscale=[[0,"#1E3A5F"],[1,"#F97316"]],
            line=dict(color="rgba(0,0,0,0)")
        ),
        text=top_states["Orders"], textposition="outside",
        textfont=dict(color="#94A3B8", size=10),
        hovertemplate="<b>%{y}</b><br>Orders: %{x}<extra></extra>",
    ))
    fig2.update_layout(**PLOTLY_LAYOUT)
    fig2.update_layout(height=320, yaxis_categoryorder="total ascending",
                       xaxis_title="", yaxis_title="")
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── Row 2: Top Products + Size demand ────────────────────────
section("Product Intelligence")
c3, c4 = st.columns([1.5, 1])

with c3:
    top_prod = fdf["Product Name"].value_counts().head(8).reset_index()
    top_prod.columns = ["Product","Count"]
    top_prod["Short"] = top_prod["Product"].str[:45] + "…"
    fig3 = go.Figure(go.Bar(
        x=top_prod["Count"], y=top_prod["Short"],
        orientation="h",
        marker=dict(color=ORANGE_PALETTE[:len(top_prod)]),
        text=top_prod["Count"], textposition="outside",
        textfont=dict(color="#94A3B8", size=10),
        hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
    ))
    fig3.update_layout(**PLOTLY_LAYOUT)
    fig3.update_layout(height=340, yaxis_categoryorder="total ascending", yaxis_tickfont_size=10,
                       title_text="Top 8 Products by Order Count",
                       title_font=dict(color="#94A3B8", size=12))
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

with c4:
    size_data = fdf["Size"].value_counts().reset_index()
    size_data.columns = ["Size","Count"]
    fig4 = px.pie(size_data, names="Size", values="Count",
                  color_discrete_sequence=MULTI_PALETTE, hole=0.5)
    fig4.update_traces(textposition="outside", textfont_size=10,
                       marker=dict(line=dict(color="#0F172A", width=2)))
    fig4.update_layout(**PLOTLY_LAYOUT, height=340,
                       title_text="Size-wise Demand",
                       title_font=dict(color="#94A3B8", size=12))
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── Row 3: Price distribution + SKU ──────────────────────────
section("Pricing & SKU Analysis")
c5, c6 = st.columns(2)

with c5:
    price_clean = fdf["Price"].dropna()
    fig5 = go.Figure(go.Histogram(
        x=price_clean, nbinsx=25,
        marker=dict(color="#F97316", line=dict(color="#0F172A", width=1)),
        hovertemplate="Price: ₹%{x}<br>Count: %{y}<extra></extra>",
    ))
    fig5.update_layout(**PLOTLY_LAYOUT, height=280,
                       xaxis_title="Price (₹)", yaxis_title="Orders",
                       title_text="Price Distribution",
                       title_font=dict(color="#94A3B8", size=12))
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

with c6:
    top_sku = fdf["SKU"].value_counts().head(10).reset_index()
    top_sku.columns = ["SKU","Orders"]
    fig6 = go.Figure(go.Bar(
        x=top_sku["SKU"], y=top_sku["Orders"],
        marker=dict(color=MULTI_PALETTE[:len(top_sku)]),
        text=top_sku["Orders"], textposition="outside",
        textfont=dict(color="#94A3B8", size=10),
    ))
    fig6.update_layout(**PLOTLY_LAYOUT, height=280,
                       xaxis_tickangle=-35, xaxis_tickfont=dict(size=9),
                       title_text="Top 10 SKUs by Orders",
                       title_font=dict(color="#94A3B8", size=12))
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── Raw data expandable ───────────────────────────────────────
section("Raw Data Explorer")
with st.expander("📄 View filtered dataset"):
    st.dataframe(fdf.reset_index(drop=True), height=320,
                 use_container_width=True)
    st.caption(f"{len(fdf):,} records shown")
