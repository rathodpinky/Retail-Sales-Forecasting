import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/Retail_Sales_Data_Unlox.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df