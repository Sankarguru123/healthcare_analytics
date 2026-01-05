import streamlit as st

def hc_render_kpis(df):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Patients", df.patient_id.nunique())
    c2.metric("Charges", f"₹{df.charges.sum():,.0f}")
    c3.metric("Collections", f"₹{df.collections.sum():,.0f}")
    c4.metric("Accounts Receivable", f"₹{df.ar_amount.sum():,.0f}")
