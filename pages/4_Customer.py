import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import *

st.set_page_config(page_title="Customer Behaviour", page_icon="👥", layout="wide")
inject_css()

sidebar_nav()


header("Customer Behaviour Analysis",
       "Survey insights from Google Forms — demographics, shopping habits, satisfaction & returns",
       "Primary Survey Data")

@st.cache_data
def load():
    df = pd.read_csv("data/E-Commerce Shopping Behavior Survey (Responses) - Form responses 1.csv")
    df.columns = df.columns.str.strip()
    return df

df = load()

# ── Column mapping (robust – match by substrings) ─────────────
def find_col(df, keywords):
    for col in df.columns:
        cl = col.lower()
        if all(k.lower() in cl for k in keywords):
            return col
    return None

COL = {
    "gender":    find_col(df, ["gender"]),
    "student":   find_col(df, ["student"]),
    "freq":      find_col(df, ["often"]),
    "platforms": find_col(df, ["platform"]),
    "products":  find_col(df, ["buy online"]) or find_col(df, ["mostly buy"]),
    "spending":  find_col(df, ["spending"]) or find_col(df, ["average spend"]),
    "reviews":   find_col(df, ["review"]),
    "cancel":    find_col(df, ["cancellation"]) or find_col(df, ["faced"]),
    "ret_reason":find_col(df, ["reason"]) or find_col(df, ["why"]),
    "delivery":  find_col(df, ["delivery option"]) or find_col(df, ["payment"]),
    "satisfy":   find_col(df, ["satisf"]),
    "returns":   find_col(df, ["return product"]) or find_col(df, ["return often"]),
    "reason_why":find_col(df, ["main reason"]) or find_col(df, ["use online"]),
}

kpi_row([
    kpi_card("📋","Total Responses",  f"{len(df)}"),
    kpi_card("📊","Survey Questions", f"{len(df.columns)-1}"),
    kpi_card("📅","Data Source",      "Google Forms"),
    kpi_card("🔍","Analysis Type",    "Primary Data"),
])

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── helpers ───────────────────────────────────────────────────
def donut(col_key, title):
    col = COL.get(col_key)
    if not col or col not in df.columns: return
    data = df[col].value_counts().reset_index()
    data.columns = ["Label","Count"]
    fig = px.pie(data, names="Label", values="Count",
                 color_discrete_sequence=MULTI_PALETTE, hole=0.55)
    fig.update_traces(textposition="outside", textfont_size=10,
                      marker=dict(line=dict(color="#0F172A", width=2)))
    layout = PLOTLY_LAYOUT.copy()
    layout.update({"height": 280,
                   "title_text": title,
                   "title_font": dict(color="#94A3B8", size=12),
                   "legend": dict(font=dict(size=9))})
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def hbar(col_key, title, multi=False):
    col = COL.get(col_key)
    if not col or col not in df.columns: return
    if multi:
        exploded = df[col].dropna().str.split(",").explode().str.strip()
        data = exploded.value_counts().reset_index()
    else:
        data = df[col].value_counts().reset_index()
    data.columns = ["Label","Count"]
    data = data.head(10)
    fig = go.Figure(go.Bar(
        x=data["Count"], y=data["Label"],
        orientation="h",
        marker=dict(color=ORANGE_PALETTE[:len(data)]),
        text=data["Count"], textposition="outside",
        textfont=dict(color="#94A3B8", size=10),
    ))
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_layout(height=280, yaxis_categoryorder="total ascending", yaxis_tickfont_size=10,
                      title_text=title, title_font=dict(color="#94A3B8", size=12))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── Section 1: Demographics ───────────────────────────────────
section("👤 Demographics")
c1, c2, c3 = st.columns(3)
with c1: donut("gender",  "Gender Distribution")
with c2: donut("student", "Student vs Non-Student")
with c3: donut("freq",    "Shopping Frequency")

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── Section 2: Platform & Product Prefs ──────────────────────
section("🛒 Platform & Product Preferences")
c1, c2 = st.columns(2)
with c1: hbar("platforms", "Platforms Used (Multi-select)", multi=True)
with c2: hbar("products",  "Products Purchased (Multi-select)", multi=True)

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── Section 3: Spending & Reviews ─────────────────────────────
section("💰 Spending & Decision Behaviour")
c1, c2, c3 = st.columns(3)
with c1: donut("spending", "Avg Spending Per Order")
with c2: donut("reviews",  "Check Reviews Before Buying?")
with c3: donut("delivery", "Preferred Delivery Option")

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── Section 4: Cancellation & Satisfaction ────────────────────
section("📦 Delivery Experience & Satisfaction")
c1, c2 = st.columns([1,1.5])
with c1: donut("cancel",  "Faced Cancellation / RTO?")
with c2: hbar("ret_reason","Reasons for Returns (Multi-select)", multi=True)

c3, c4 = st.columns(2)
with c3: donut("satisfy",   "Customer Satisfaction Level")
with c4: donut("returns",   "Do You Return Products Often?")

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── Section 5: Why online? ────────────────────────────────────
section("🎯 Main Reason for Online Shopping")
hbar("reason_why", "Primary Reason Customers Shop Online")

# ── Raw data ──────────────────────────────────────────────────
st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)
section("Raw Survey Data")
with st.expander("📄 View survey responses"):
    st.dataframe(df, height=320, use_container_width=True)
    st.caption(f"{len(df)} responses · {len(df.columns)} questions")
