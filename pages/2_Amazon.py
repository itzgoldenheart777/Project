import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import *

st.set_page_config(page_title="Amazon Analytics", page_icon="\U0001F4E6", layout="wide")
inject_css()

sidebar_nav()

header("Amazon Sales Analytics", "Category performance, revenue trends & state-level insights · 2022", badge="Amazon Platform", logo="amazon")

@st.cache_data
def load():
    df = pd.read_csv("data/Amazon Sale Report.csv", low_memory=False)
    df.columns = df.columns.str.strip()
    df["Date"]   = pd.to_datetime(df["Date"], errors="coerce", dayfirst=False)
    df["Month"]  = df["Date"].dt.month
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Qty"]    = pd.to_numeric(df["Qty"], errors="coerce")
    df["Order_Value"] = df["Qty"] * df["Amount"]
    df["ship-state"] = df["ship-state"].str.upper().str.strip()
    return df

df = load()

with st.sidebar:
    st.markdown('<hr style="border-color:#2E3A4E;margin:16px 0 12px">', unsafe_allow_html=True)
    st.markdown('<div style="color:#8A94A6;font-size:0.72rem;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">Filters</div>', unsafe_allow_html=True)
    cats = ["All"] + sorted(df["Category"].dropna().unique().tolist())
    sel_cat = st.selectbox("Category", cats)
    fuls = ["All"] + sorted(df["Fulfilment"].dropna().unique().tolist())
    sel_ful = st.selectbox("Fulfilment", fuls)
    months = ["All"] + [str(m) for m in sorted(df["Month"].dropna().unique().tolist())]
    sel_mon = st.selectbox("Month", months)

fdf = df.copy()
if sel_cat != "All": fdf = fdf[fdf["Category"] == sel_cat]
if sel_ful != "All": fdf = fdf[fdf["Fulfilment"] == sel_ful]
if sel_mon != "All": fdf = fdf[fdf["Month"] == int(sel_mon)]

total   = len(fdf)
del_cnt = fdf["Status"].str.contains("Delivered", na=False).sum()
cancel  = (fdf["Status"] == "Cancelled").sum()
revenue = fdf["Amount"].sum()
qty_tot = fdf["Qty"].sum()
avg_rev = fdf["Amount"].mean()

kpi_row([
    kpi_card("\U0001F4E6", "Total Orders",    f"{total:,}"),
    kpi_card("\u2705", "Delivered",       f"{del_cnt:,}",   delta=f"{del_cnt/total*100:.1f}%" if total else "0%",    delta_pos=True),
    kpi_card("\u274C", "Cancelled",       f"{cancel:,}",    delta=f"{cancel/total*100:.1f}%"  if total else "0%",    delta_pos=False),
    kpi_card("\U0001F4E6", "Units Sold",      f"{int(qty_tot):,}"),
    kpi_card("\U0001F4B0", "Total Revenue",   f"₹{revenue/1e7:.2f}Cr"),
    kpi_card("\U0001F4CA", "Avg Order Value", f"₹{avg_rev:.0f}"),
])

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

section("Revenue & Category Analysis")
c1, c2 = st.columns([1.6, 1])

with c1:
    monthly = fdf.groupby("Month")["Amount"].sum().reset_index()
    month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                 7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    monthly["Month_Name"] = monthly["Month"].map(month_map)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly["Month_Name"], y=monthly["Amount"],
        marker=dict(color=monthly["Amount"],
                    colorscale=[[0,"#2E3A4E"],[1,"#F8BE14"]],
                    line=dict(color="rgba(0,0,0,0)")),
        hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=monthly["Month_Name"], y=monthly["Amount"],
        mode="lines+markers",
        line=dict(color="#4E7CFF", width=2, dash="dot"),
        marker=dict(size=6, color="#4E7CFF"),
        hoverinfo="skip", name="trend",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=300,
                      yaxis_tickprefix="₹", yaxis_tickformat=".2s",
                      title_text="Monthly Revenue", title_font=dict(color="#8A94A6", size=12),
                      showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    cat_rev = fdf.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(8).reset_index()
    cat_rev.columns = ["Category","Revenue"]
    fig2 = px.pie(cat_rev, names="Category", values="Revenue",
                  color_discrete_sequence=MULTI_PALETTE, hole=0.5)
    fig2.update_traces(textposition="outside", textfont_size=10,
                       marker=dict(line=dict(color="#141828", width=2)))
    fig2.update_layout(**PLOTLY_LAYOUT, height=300,
                       title_text="Revenue by Category",
                       title_font=dict(color="#8A94A6", size=12))
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

section("Order Status & Geographic Distribution")
c3, c4 = st.columns([1, 1.4])

with c3:
    status_grp = fdf["Status"].value_counts().head(7).reset_index()
    status_grp.columns = ["Status","Count"]
    status_grp["Short"] = status_grp["Status"].str.replace("Shipped - ", "", regex=False)
    fig3 = go.Figure(go.Bar(
        x=status_grp["Count"], y=status_grp["Short"],
        orientation="h",
        marker=dict(color=MULTI_PALETTE[:len(status_grp)]),
        text=status_grp["Count"].apply(lambda x: f"{x:,}"),
        textposition="outside", textfont=dict(color="#8A94A6", size=10),
        hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>",
    ))
    fig3.update_layout(**PLOTLY_LAYOUT)
    fig3.update_layout(height=300, yaxis_categoryorder="total ascending", yaxis_tickfont_size=9,
                       title_text="Order Status Breakdown",
                       title_font=dict(color="#8A94A6", size=12))
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

with c4:
    state_rev = (fdf.groupby("ship-state")["Amount"].sum()
                   .sort_values(ascending=False).head(12).reset_index())
    state_rev.columns = ["State","Revenue"]
    fig4 = go.Figure(go.Bar(
        x=state_rev["Revenue"], y=state_rev["State"],
        orientation="h",
        marker=dict(color=state_rev["Revenue"],
                    colorscale=[[0,"#2E3A4E"],[0.5,"#4E7CFF"],[1,"#F8BE14"]],
                    line=dict(color="rgba(0,0,0,0)")),
        text=state_rev["Revenue"].apply(lambda x: f"₹{x/1e5:.1f}L"),
        textposition="outside", textfont=dict(color="#8A94A6", size=10),
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
    ))
    fig4.update_layout(**PLOTLY_LAYOUT)
    fig4.update_layout(height=300, yaxis_categoryorder="total ascending", yaxis_tickfont_size=10,
                       title_text="Top States by Revenue",
                       title_font=dict(color="#8A94A6", size=12))
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

section("Fulfilment & Order Value Distribution")
c5, c6 = st.columns(2)

with c5:
    ful_data = fdf["Fulfilment"].value_counts().reset_index()
    ful_data.columns = ["Fulfilment","Count"]
    fig5 = px.pie(ful_data, names="Fulfilment", values="Count",
                  color_discrete_sequence=["#F8BE14","#4E7CFF","#8651CA"],
                  hole=0.55)
    fig5.update_traces(textfont_size=11,
                       marker=dict(line=dict(color="#141828", width=2)))
    fig5.update_layout(**PLOTLY_LAYOUT, height=270,
                       title_text="Fulfilment Method Split",
                       title_font=dict(color="#8A94A6", size=12))
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

with c6:
    cat_qty = fdf.groupby("Category")["Qty"].sum().sort_values(ascending=False).head(8).reset_index()
    cat_qty.columns = ["Category","Units"]
    fig6 = go.Figure(go.Bar(
        x=cat_qty["Category"], y=cat_qty["Units"],
        marker=dict(color=ORANGE_PALETTE[:len(cat_qty)]),
        text=cat_qty["Units"].apply(lambda x: f"{x:,}"),
        textposition="outside", textfont=dict(color="#8A94A6", size=10),
    ))
    fig6.update_layout(**PLOTLY_LAYOUT, height=270,
                       xaxis_tickangle=-30, xaxis_tickfont=dict(size=10),
                       title_text="Units Sold by Category",
                       title_font=dict(color="#8A94A6", size=12))
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)
section("Raw Data Explorer")
with st.expander("\U0001F4C4 View filtered dataset"):
    st.dataframe(fdf[["Date","Status","Fulfilment","Category","Size","Qty","Amount","ship-state"]].reset_index(drop=True),
                 height=320, use_container_width=True)
    st.caption(f"{len(fdf):,} records · Revenue ₹{fdf['Amount'].sum():,.2f}")
