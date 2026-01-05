import plotly.express as px
import streamlit as st
import pandas as pd

# --------------------------------------------------
# 1️⃣ BAR CHART – Revenue by Department
# --------------------------------------------------
def hc_revenue_bar(df):
    rev = (
        df.groupby("department")[["charges", "collections"]]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        rev,
        x="department",
        y=["charges", "collections"],
        barmode="group",
        title="Revenue by Department",
        template="plotly_dark"
    )

    st.plotly_chart(fig, width="stretch")


# --------------------------------------------------
# 2️⃣ PIE CHART – Charges Distribution
# --------------------------------------------------
def hc_revenue_pie(df):
    rev = df.groupby("department", as_index=False)["charges"].sum()

    fig = px.pie(
        rev,
        names="department",
        values="charges",
        title="Charges Distribution by Department",
        template="plotly_dark"
    )

    st.plotly_chart(fig, width="stretch")


# --------------------------------------------------
# 3️⃣ DONUT CHART – Collections Distribution
# --------------------------------------------------
def hc_revenue_donut(df):
    rev = df.groupby("department", as_index=False)["collections"].sum()

    fig = px.pie(
        rev,
        names="department",
        values="collections",
        hole=0.4,
        title="Collections Distribution (Donut)",
        template="plotly_dark"
    )

    st.plotly_chart(fig, width="stretch")


# --------------------------------------------------
# 4️⃣ LINE CHART – Revenue Trend (Time Series)
# --------------------------------------------------
def hc_revenue_trend(df):
    df["visit_date"] = pd.to_datetime(df["visit_date"])

    trend = (
        df.groupby("visit_date")[["charges", "collections"]]
        .sum()
        .reset_index()
    )

    fig = px.line(
        trend,
        x="visit_date",
        y=["charges", "collections"],
        title="Revenue Trend Over Time",
        template="plotly_dark"
    )

    st.plotly_chart(fig, width="stretch")


# --------------------------------------------------
# 5️⃣ STACKED BAR – Charges vs Collections
# --------------------------------------------------
def hc_revenue_stacked(df):
    rev = (
        df.groupby("department")[["charges", "collections"]]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        rev,
        x="department",
        y=["charges", "collections"],
        barmode="stack",
        title="Charges vs Collections (Stacked)",
        template="plotly_dark"
    )

    st.plotly_chart(fig, width="stretch")
