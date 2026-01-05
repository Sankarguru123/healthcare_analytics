import plotly.express as px
import streamlit as st

def hc_payment_chart(df):
    fig = px.pie(
        df,
        names="payment_status",
        hole=0.4,
        template="plotly_dark"
    )

    st.plotly_chart(fig, width='stretch')
