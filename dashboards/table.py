from st_aggrid import AgGrid, GridOptionsBuilder
import streamlit as st

def hc_data_table(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gb.configure_default_column(filter=True, sortable=True)
    AgGrid(df, gridOptions=gb.build(), height=450, theme="balham-dark")
