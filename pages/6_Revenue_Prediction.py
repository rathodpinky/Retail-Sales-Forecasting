import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

from utils.load_data import load_data

st.set_page_config(
    page_title="Revenue Prediction",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Revenue Prediction")

st.markdown("---")

df = load_data()

# Load trained model
model = joblib.load("models/Retail_Final_Model.pkl")

# Load scaler
scaler = joblib.load("models/standard_scaler.pkl")

st.subheader("Enter Product Details")

col1, col2 = st.columns(2)

with col1:

    store = st.selectbox(
        "Store",
        sorted(df["Store_ID"].unique())
    )

    region = st.selectbox(
        "Region",
        sorted(df["Region"].unique())
    )

    category = st.selectbox(
        "Product Category",
        sorted(df["Product_Category"].unique())
    )

    subcategory = st.selectbox(
        "Product Subcategory",
        sorted(df["Product_Subcategory"].unique())
    )

    brand = st.selectbox(
        "Brand",
        sorted(df["Brand"].unique())
    )

with col2:

    customer = st.selectbox(
        "Customer Type",
        sorted(df["Customer_Type"].unique())
    )

    payment = st.selectbox(
        "Payment Mode",
        sorted(df["Payment_Mode"].unique())
    )

    promotion = st.selectbox(
        "Promotion Applied",
        sorted(df["Promotion_Applied"].unique())
    )

    holiday = st.selectbox(
        "Holiday",
        sorted(df["Holiday_Flag"].unique())
    )

col3, col4 = st.columns(2)

with col3:

    unit_price = st.number_input(
        "Unit Price",
        min_value=0.0,
        value=1000.0
    )

    units_sold = st.number_input(
        "Units Sold",
        min_value=1,
        value=10
    )

    discount = st.slider(
        "Discount %",
        0,
        80,
        10
    )

with col4:

    stock = st.number_input(
        "Stock On Hand",
        min_value=0,
        value=100
    )

    rating = st.slider(
        "Store Rating",
        1.0,
        5.0,
        4.0
    )

