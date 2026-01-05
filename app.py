import streamlit as st
import pandas as pd
from datetime import date, timedelta

from utils.db import hc_get_engine
from utils.rls import hc_apply_rls,hc_get_users
from etl.extract import hc_extract_csv
from etl.transform import hc_transform
from etl.load import hc_incremental_load

from dashboards.kpis import hc_render_kpis
from dashboards.revenue import hc_revenue_bar,hc_revenue_pie,hc_revenue_donut,hc_revenue_trend,hc_revenue_stacked
from dashboards.payments import hc_payment_chart
from dashboards.table import hc_data_table
from sqlalchemy import text

engine = hc_get_engine()

st.set_page_config(page_title="Healthcare BI", layout="wide")

# # ---------------- THEME ----------------
# st.markdown("""
# <style>
# body { background-color: #0E1117; }
# [data-testid="stMetric"] {
#     background-color: #1F2937;
#     padding: 18px;
#     border-radius: 10px;
# }
# [data-testid="stSidebar"] { background-color: #111827; }
# h1, h2, h3, h4, label { color: #E5E7EB; }
# </style>
# """, unsafe_allow_html=True)




st.markdown("""
<style>
/* -------- Main App Background -------- */
.stApp {
    background: linear-gradient(135deg, #0F172A, #020617);
    color: #E5E7EB;
}

/* -------- Sidebar -------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid #1F2937;
}

/* -------- Sidebar Text -------- */
section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

/* -------- Header Titles -------- */
h1, h2, h3, h4 {
    color: #F9FAFB;
    font-weight: 600;
}

/* -------- KPI Cards -------- */
[data-testid="stMetric"] {
    background: #020617;
    border: 1px solid #1F2937;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}

/* -------- Tabs -------- */
button[data-baseweb="tab"] {
    background-color: #020617;
    border-radius: 10px;
    margin-right: 6px;
    padding: 10px 16px;
    border: 1px solid #1F2937;
    color: #E5E7EB;
}

/* Active Tab */
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    color: white;
    font-weight: 600;
}

/* -------- Buttons -------- */
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    color: white;
    border-radius: 10px;
    padding: 8px 16px;
    border: none;
    font-weight: 600;
}

/* Hover effect */
.stButton > button:hover {
    background: linear-gradient(135deg, #1E40AF, #1D4ED8);
    transform: scale(1.03);
}

/* -------- Selectbox / Multiselect -------- */
div[data-baseweb="select"] {
    background-color: #020617;
    border-radius: 8px;
}

/* -------- Data Table -------- */
.ag-theme-balham-dark {
    --ag-background-color: #020617;
    --ag-header-background-color: #020617;
    --ag-odd-row-background-color: #020617;
    --ag-border-color: #1F2937;
}

/* -------- Scrollbar -------- */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #2563EB;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 🔐 Power BI Controls")

users = hc_get_users(engine)
user = st.sidebar.selectbox(
    "View As User",
    users
)

range_start = st.sidebar.date_input(
    "RangeStart",
    value=date.today() - timedelta(days=30)
)

range_end = st.sidebar.date_input(
    "RangeEnd",
    value=date.today(),
    max_value= date.today(),
)


file = st.sidebar.file_uploader(
    "Upload Healthcare CSV", type="csv"
)

# ---------------- INCREMENTAL LOAD ----------------
if file:
    df_raw = hc_extract_csv(file)
    df_transformed = hc_transform(df_raw)
    hc_incremental_load(df_transformed, engine, range_start, range_end)
    st.sidebar.success("Incremental Refresh Done")



st.sidebar.markdown("### 🗑️ Data Management")

delete_all = st.sidebar.checkbox("Delete all existing records")

if delete_all:
    if st.sidebar.button("Confirm Delete"):
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE fact_billing"))
        st.sidebar.success("✅ All records deleted successfully")
        st.stop()

# ---------------- READ DATA (FIXED) ----------------
from sqlalchemy import text

from sqlalchemy import text

df = pd.read_sql(
    text("""
        SELECT *
        FROM fact_billing
        WHERE visit_date >= :start_date
          AND visit_date < :end_date
    """),
    engine,
    params={
        "start_date": range_start,
        "end_date": range_end
    }
)

# ---------------- ROW LEVEL SECURITY ----------------
df = hc_apply_rls(df, engine, user)

# ---------------- DEPARTMENT FILTER ----------------
dept = st.sidebar.multiselect(
    "Department",
    options=df["department"].unique(),
    default=df["department"].unique()
)

df = df[df["department"].isin(dept)]

# ---------------- DASHBOARD ----------------
st.markdown(f"## 🏥 Healthcare Dashboard ({user})")

hc_render_kpis(df)

tab1, tab2, tab3 = st.tabs(
    ["📊 Revenue", "⏳ Payments", "📋 Table"]
)

with tab1:
    hc_revenue_bar(df)
    hc_revenue_pie(df)
    hc_revenue_stacked(df)
    hc_revenue_trend(df)
    hc_revenue_donut(df)

with tab2:
    hc_payment_chart(df)

with tab3:
    hc_data_table(df)
