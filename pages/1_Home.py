import streamlit as st
import plotly.express as px
from utils.load_data import load_data


df = load_data()

st.title("🏠 Home Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${df['Revenue'].sum():,.2f}"
)

col2.metric(
    "Total Sales",
    f"${df['Total_Sales'].sum():,.2f}"
)

col3.metric(
    "Units Sold",
    f"{df['Units_Sold'].sum():,}"
)

col4.metric(
    "Stores",
    df["Store_ID"].nunique()
)

monthly = (
    df.groupby(df["Date"].dt.to_period("M"))["Revenue"]
      .sum()
      .reset_index()
)

monthly["Date"] = monthly["Date"].astype(str)

fig = px.line(
    monthly,
    x="Date",
    y="Revenue",
    title="Monthly Revenue Trend",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

region = (
    df.groupby("Region")["Revenue"]
      .sum()
      .reset_index()
)

fig = px.bar(
    region,
    x="Region",
    y="Revenue",
    title="Revenue by Region"
)

st.plotly_chart(fig, use_container_width=True)


category = (
    df.groupby("Product_Category")["Revenue"]
      .sum()
      .reset_index()
)

fig = px.pie(
    category,
    names="Product_Category",
    values="Revenue",
    title="Revenue by Product Category"
)

st.plotly_chart(fig, use_container_width=True)


products = (
    df.groupby("Product_ID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig = px.bar(
    products,
    x="Product_ID",
    y="Revenue",
    title="Top 10 Products"
)

st.plotly_chart(fig, use_container_width=True)