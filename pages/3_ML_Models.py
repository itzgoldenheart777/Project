import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import *

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="ML Model Training", page_icon="🤖", layout="wide")
inject_css()

sidebar_nav()
with st.sidebar:
    st.markdown('<hr style="border-color:#1E3A5F;margin:16px 0 12px">', unsafe_allow_html=True)
    st.markdown('<div style="color:var(--text-muted);font-size:0.72rem;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">Training Config</div>', unsafe_allow_html=True)
    test_size  = st.slider("Test Set Size", 0.1, 0.4, 0.2, 0.05, help="Fraction of data for testing")
    run_btn    = st.button("▶  Run Training", use_container_width=True, type="primary")


header("ML Model Training & Evaluation",
       "Train Logistic Regression, Decision Tree & Random Forest — compare accuracy, precision, recall & F1",
       "Machine Learning")

# ── Load + prepare ────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/Amazon Sale Report.csv", low_memory=False)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=False)
    df["Month"] = df["Date"].dt.month
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["Order_Value"] = df["Qty"] * df["Amount"]
    df = df.dropna(subset=["Category","Qty","Amount","Fulfilment","Status","Month"])
    return df

raw = load_data()

# ── Info banner ───────────────────────────────────────────────
kpi_row([
    kpi_card("📊","Total Records",   f"{len(raw):,}"),
    kpi_card("🎯","Features Used",   "6"),
    kpi_card("🏷️","Target Classes", f"{raw['Status'].nunique()}"),
    kpi_card("🔀","Train Split",     f"{int((1-test_size)*100)}%"),
    kpi_card("🧪","Test Split",      f"{int(test_size*100)}%"),
])

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── Feature overview ──────────────────────────────────────────
section("Dataset & Feature Engineering")
c1, c2 = st.columns([1.2, 1])
with c1:
    feat_df = pd.DataFrame({
        "Feature":       ["Category","Qty","Amount","Fulfilment","Month","Order_Value"],
        "Type":          ["Categorical (encoded)","Numerical","Numerical","Categorical (encoded)","Numerical","Engineered"],
        "Description":   ["Product category","Units ordered","Order amount ₹","Fulfilment method","Month of order","Qty × Amount"],
    })
    st.dataframe(feat_df, use_container_width=True, hide_index=True, height=230)

with c2:
    status_dist = raw["Status"].value_counts().head(7).reset_index()
    status_dist.columns = ["Status","Count"]
    status_dist["Short"] = status_dist["Status"].str.replace("Shipped - ", "", regex=False)
    fig_sd = go.Figure(go.Bar(
        x=status_dist["Count"], y=status_dist["Short"],
        orientation="h",
        marker=dict(color=MULTI_PALETTE[:len(status_dist)]),
        text=status_dist["Count"].apply(lambda x: f"{x:,}"),
        textposition="outside", textfont=dict(color="#94A3B8", size=10),
    ))
    fig_sd.update_layout(**PLOTLY_LAYOUT)
    fig_sd.update_layout(height=230, yaxis_categoryorder="total ascending", yaxis_tickfont_size=9,
                         title_text="Target Class Distribution",
                         title_font=dict(color="#94A3B8", size=12))
    st.plotly_chart(fig_sd, use_container_width=True, config={"displayModeBar": False})

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── TRAIN ─────────────────────────────────────────────────────
if run_btn or "ml_results" in st.session_state:
    if run_btn:
        # prepare
        data = raw.copy()
        le_cat = LabelEncoder(); le_ful = LabelEncoder(); le_status = LabelEncoder()
        data["Category"]  = le_cat.fit_transform(data["Category"])
        data["Fulfilment"] = le_ful.fit_transform(data["Fulfilment"])
        data["Status"]    = le_status.fit_transform(data["Status"])
        X = data[["Category","Qty","Amount","Fulfilment","Month","Order_Value"]]
        y = data["Status"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        with st.spinner("Training models…"):
            models = {
                "Logistic Regression": LogisticRegression(max_iter=500),
                "Decision Tree":       DecisionTreeClassifier(max_depth=12, random_state=42),
                "Random Forest":       RandomForestClassifier(n_estimators=80, max_depth=12, random_state=42),
            }
            results = []
            trained = {}
            for name, mdl in models.items():
                mdl.fit(X_train, y_train)
                preds = mdl.predict(X_test)
                results.append({
                    "Model":     name,
                    "Accuracy":  accuracy_score(y_test, preds),
                    "Precision": precision_score(y_test, preds, average="weighted", zero_division=0),
                    "Recall":    recall_score(y_test, preds, average="weighted", zero_division=0),
                    "F1 Score":  f1_score(y_test, preds, average="weighted", zero_division=0),
                })
                trained[name] = (mdl, preds)

        res_df = pd.DataFrame(results)
        best_name = res_df.sort_values("Accuracy", ascending=False).iloc[0]["Model"]
        best_model, best_preds = trained[best_name]

        # feature importance
        fi = None
        if hasattr(best_model, "feature_importances_"):
            fi = pd.DataFrame({
                "Feature":    ["Category","Qty","Amount","Fulfilment","Month","Order_Value"],
                "Importance": best_model.feature_importances_,
            }).sort_values("Importance", ascending=False)

        cm = confusion_matrix(y_test, best_preds)
        classes = [str(c) for c in le_status.classes_[:cm.shape[0]]]

        st.session_state["ml_results"] = {
            "res_df": res_df, "best_name": best_name,
            "cm": cm, "classes": classes, "fi": fi,
            "le_status": le_status,
        }

    # ── Display results ───────────────────────────────────────
    r = st.session_state["ml_results"]
    res_df    = r["res_df"]
    best_name = r["best_name"]
    cm        = r["cm"]
    classes   = r["classes"]
    fi        = r["fi"]

    section("Model Performance Comparison")

    # Metric cards for best model
    best_row = res_df[res_df["Model"] == best_name].iloc[0]
    kpi_row([
        kpi_card("🏆","Best Model",   best_name),
        kpi_card("🎯","Accuracy",     f"{best_row['Accuracy']:.2%}"),
        kpi_card("📐","Precision",    f"{best_row['Precision']:.2%}"),
        kpi_card("📡","Recall",       f"{best_row['Recall']:.2%}"),
        kpi_card("⚖️","F1 Score",    f"{best_row['F1 Score']:.2%}"),
    ])

    # Table + radar
    c1, c2 = st.columns([1.1, 1])
    with c1:
        disp = res_df.copy()
        for col in ["Accuracy","Precision","Recall","F1 Score"]:
            disp[col] = disp[col].map(lambda x: f"{x:.4f}")
        st.dataframe(disp.set_index("Model"), use_container_width=True)

    with c2:
        metrics = ["Accuracy","Precision","Recall","F1 Score"]
        fig_radar = go.Figure()
        colors = ["#F97316","#38BDF8","#A78BFA"]
        fill_colors = ["rgba(249, 115, 22, 0.15)", "rgba(56, 189, 248, 0.15)", "rgba(167, 139, 250, 0.15)"]
        for i, row in res_df.iterrows():
            vals = [row[m] for m in metrics]
            vals += vals[:1]
            cats  = metrics + [metrics[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals, theta=cats, fill="toself", name=row["Model"],
                line_color=colors[i % len(colors)],
                fillcolor=fill_colors[i % len(fill_colors)],
            ))
        fig_radar.update_layout(**PLOTLY_LAYOUT, height=280,
                                polar=dict(
                                    bgcolor="rgba(0,0,0,0)",
                                    angularaxis=dict(tickfont=dict(color="#94A3B8", size=10), linecolor="#1E3A5F"),
                                    radialaxis=dict(tickfont=dict(color="#64748B", size=9), gridcolor="#1E3A5F",
                                                    range=[0,1], linecolor="#1E3A5F"),
                                ))
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)
    section("Accuracy Bar Comparison")
    fig_bar = go.Figure(go.Bar(
        x=res_df["Model"], y=res_df["Accuracy"],
        marker=dict(color=["#F97316" if n == best_name else "#2D4A7A" for n in res_df["Model"]],
                    line=dict(color="rgba(0,0,0,0)")),
        text=res_df["Accuracy"].map(lambda x: f"{x:.2%}"),
        textposition="outside", textfont=dict(color="#F1F5F9", size=12),
    ))
    fig_bar.update_layout(**PLOTLY_LAYOUT, height=250,
                          yaxis_tickformat=".0%", yaxis_range=[0, 1.15])
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

    # ── Confusion matrix + feature importance ─────────────────
    ca, cb = st.columns(2)
    with ca:
        section("Confusion Matrix")
        max_display = 8
        cm_small = cm[:max_display, :max_display]
        cls_small = classes[:max_display]
        fig_cm = px.imshow(cm_small, x=cls_small, y=cls_small,
                           color_continuous_scale=[[0,"#0F172A"],[0.5,"#1E3A5F"],[1,"#F97316"]],
                           text_auto=True, aspect="auto")
        fig_cm.update_layout(**PLOTLY_LAYOUT, height=320,
                             coloraxis_showscale=False,
                             xaxis_tickfont=dict(size=9),
                             yaxis_tickfont=dict(size=9))
        fig_cm.update_traces(textfont=dict(color="white", size=10))
        st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})

    with cb:
        section("Feature Importance")
        if fi is not None:
            fig_fi = go.Figure(go.Bar(
                x=fi["Importance"], y=fi["Feature"],
                orientation="h",
                marker=dict(color=ORANGE_PALETTE[:len(fi)]),
                text=fi["Importance"].map(lambda x: f"{x:.3f}"),
                textposition="outside", textfont=dict(color="#94A3B8", size=10),
            ))
            fig_fi.update_layout(**PLOTLY_LAYOUT)
            fig_fi.update_layout(height=320, yaxis_categoryorder="total ascending")
            st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Feature importance is available for tree-based models.")

else:
    st.markdown("""
    <div style="text-align:center;padding:60px;background:#1E293B;border:1px dashed #1E3A5F;border-radius:16px;margin-top:20px">
        <div style="font-size:3rem;margin-bottom:16px">🤖</div>
        <div style="color:#F1F5F9;font-size:1.1rem;font-weight:600;margin-bottom:8px">Ready to Train</div>
        <div style="color:#64748B;font-size:0.875rem">Click <b style="color:#F97316">▶ Run Training</b> in the sidebar to start ML model comparison</div>
    </div>""", unsafe_allow_html=True)
