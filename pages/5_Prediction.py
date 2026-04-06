import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import *

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Order Prediction", page_icon="\U0001F52E", layout="wide")
inject_css()

sidebar_nav()

header("Order Status Prediction",
       "Enter order details to predict delivery outcome using Random Forest ML model",
       "Live Prediction")

@st.cache_resource
def build_model():
    df = pd.read_csv("data/Amazon Sale Report.csv", low_memory=False)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=False)
    df["Month"] = df["Date"].dt.month
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["Order_Value"] = df["Qty"] * df["Amount"]
    df = df.dropna(subset=["Category","Qty","Amount","Fulfilment","Status","Month"])

    le_cat = LabelEncoder(); le_ful = LabelEncoder(); le_status = LabelEncoder()
    df["Category_enc"]  = le_cat.fit_transform(df["Category"])
    df["Fulfilment_enc"] = le_ful.fit_transform(df["Fulfilment"])
    df["Status_enc"]    = le_status.fit_transform(df["Status"])

    X = df[["Category_enc","Qty","Amount","Fulfilment_enc","Month","Order_Value"]]
    y = df["Status_enc"]

    model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    model.fit(X, y)

    return model, le_cat, le_ful, le_status, df

model, le_cat, le_ful, le_status, df = build_model()

STATUS_STYLE = {
    "Shipped - Delivered to Buyer":    ("\u2705", "#22C55E", "Order successfully delivered to the buyer."),
    "Shipped":                         ("\U0001F69A", "#4E7CFF", "Order is in transit and on the way."),
    "Cancelled":                       ("\u274C", "#EF4444", "Order was cancelled before delivery."),
    "Shipped - Returned to Seller":    ("\U0001F504", "#F8BE14", "Order was shipped back to the seller."),
    "Pending":                         ("\u23F3", "#F8BE14", "Order is pending processing."),
    "Pending - Waiting for Pick Up":   ("\U0001F4E6", "#8651CA", "Waiting for courier pickup."),
    "Shipped - Returning to Seller":   ("\u21A9\uFE0F", "#F472B6", "Order is on its way back to seller."),
    "Shipped - Out for Delivery":      ("\U0001F6F5", "#4ADE80", "Out for delivery — arriving soon!"),
}
DEFAULT_STYLE = ("\U0001F4CB", "#8A94A6", "Order status determined.")

kpi_row([
    kpi_card("\U0001F4CA","Training Records", f"{len(df):,}"),
    kpi_card("\U0001F916","Algorithm",        "Random Forest"),
    kpi_card("\U0001F333","Estimators",       "100 trees"),
    kpi_card("\U0001F3AF","Features",         "6 input features"),
    kpi_card("\U0001F3F7\uFE0F","Output Classes",  f"{le_status.classes_.shape[0]}"),
])

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

section("Enter Order Details")

col_form, col_result = st.columns([1, 1])

with col_form:
    cats_available = sorted(le_cat.classes_.tolist())
    fuls_available = sorted(le_ful.classes_.tolist())

    category   = st.selectbox("\U0001F4C1 Product Category", cats_available)
    fulfilment = st.selectbox("\U0001F3ED Fulfilment Method", fuls_available)
    qty        = st.number_input("\U0001F4E6 Quantity (units)", min_value=1, max_value=50, value=1, step=1)
    amount     = st.number_input("\U0001F4B0 Order Amount (₹)", min_value=1.0, max_value=50000.0, value=599.0, step=50.0)
    month      = st.select_slider("\U0001F4C5 Order Month",
                                   options=list(range(1, 13)),
                                   value=6,
                                   format_func=lambda m: ["Jan","Feb","Mar","Apr","May","Jun",
                                                           "Jul","Aug","Sep","Oct","Nov","Dec"][m-1])

    order_value = qty * amount
    st.markdown(f'<div style="background:#22293A;border:1px solid #2E3A4E;border-radius:10px;padding:12px 16px;margin-top:4px;color:#F0EEE8"><span style="color:#8A94A6;font-size:0.8rem">Computed Order Value → </span><b style="color:#F8BE14">₹{order_value:,.2f}</b></div>', unsafe_allow_html=True)

    predict_btn = st.button("\U0001F52E  Predict Order Status", use_container_width=True, type="primary")

with col_result:
    if predict_btn:
        cat_enc = le_cat.transform([category])[0]
        ful_enc = le_ful.transform([fulfilment])[0]
        sample  = pd.DataFrame([[cat_enc, qty, amount, ful_enc, month, order_value]],
                               columns=["Category_enc","Qty","Amount","Fulfilment_enc","Month","Order_Value"])
        pred_enc   = model.predict(sample)[0]
        pred_proba = model.predict_proba(sample)[0]
        status     = le_status.inverse_transform([pred_enc])[0]
        confidence = pred_proba.max() * 100

        icon, color, message = STATUS_STYLE.get(status, DEFAULT_STYLE)

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#22293A,#1A1F2E);
                    border:1px solid {color};border-radius:16px;
                    padding:32px;text-align:center;margin-top:8px">
            <div style="font-size:3rem;margin-bottom:12px">{icon}</div>
            <div style="color:#8A94A6;font-size:0.8rem;letter-spacing:1px;
                        text-transform:uppercase;margin-bottom:8px">Predicted Status</div>
            <div style="color:{color};font-size:1.35rem;font-weight:700;
                        margin-bottom:12px;line-height:1.3">{status}</div>
            <div style="color:#8A94A6;font-size:0.85rem;margin-bottom:20px">{message}</div>
            <div style="background:rgba(0,0,0,0.3);border-radius:10px;padding:10px 16px;
                        display:inline-block">
                <span style="color:#8A94A6;font-size:0.75rem">Model Confidence</span>
                <span style="color:#F0EEE8;font-size:1.2rem;font-weight:700;margin-left:10px">{confidence:.1f}%</span>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div style="margin-top:20px">', unsafe_allow_html=True)
        section("Probability Breakdown (Top 6)")
        top_n = 6
        sorted_idx = np.argsort(pred_proba)[::-1][:top_n]
        top_labels = [le_status.classes_[i] for i in sorted_idx]
        top_probs  = [pred_proba[i] * 100 for i in sorted_idx]
        top_short  = [l.replace("Shipped - ","") for l in top_labels]

        fig = go.Figure(go.Bar(
            x=top_probs, y=top_short, orientation="h",
            marker=dict(
                color=["#F8BE14" if l == status else "#2E3A4E" for l in top_labels],
                line=dict(color="rgba(0,0,0,0)")
            ),
            text=[f"{p:.1f}%" for p in top_probs],
            textposition="outside", textfont=dict(color="#8A94A6", size=10),
        ))
        fig.update_layout(**PLOTLY_LAYOUT)
        fig.update_layout(height=260, yaxis_categoryorder="total ascending", yaxis_tickfont_size=10, xaxis_ticksuffix="%")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:#22293A;border:1px dashed #2E3A4E;border-radius:16px;
                    padding:60px 30px;text-align:center;margin-top:8px">
            <div style="font-size:3rem;margin-bottom:16px">\U0001F52E</div>
            <div style="color:#F0EEE8;font-weight:600;font-size:1rem;margin-bottom:8px">
                Awaiting Prediction</div>
            <div style="color:#8A94A6;font-size:0.85rem">
                Fill in the order details on the left and click<br>
                <b style="color:#F8BE14">Predict Order Status</b> to see results
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

section("Feature Importance (Random Forest)")
fi_df = pd.DataFrame({
    "Feature":    ["Category","Qty","Amount","Fulfilment","Month","Order_Value"],
    "Importance": model.feature_importances_,
}).sort_values("Importance", ascending=True)

fig_fi = go.Figure(go.Bar(
    x=fi_df["Importance"], y=fi_df["Feature"],
    orientation="h",
    marker=dict(color=fi_df["Importance"],
                colorscale=[[0,"#2E3A4E"],[1,"#F8BE14"]],
                line=dict(color="rgba(0,0,0,0)")),
    text=fi_df["Importance"].map(lambda x: f"{x:.3f}"),
    textposition="outside", textfont=dict(color="#8A94A6", size=11),
))
fig_fi.update_layout(**PLOTLY_LAYOUT, height=240,
                     xaxis_tickformat=".3f")
st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})
