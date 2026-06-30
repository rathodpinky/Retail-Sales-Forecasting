import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_data

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Product Analytics",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Product Analytics Dashboard")

st.markdown("---")

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("🔍 Product Filters")

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Category",
    sorted(df["Product_Category"].unique()),
    default=sorted(df["Product_Category"].unique())
)

brands = st.sidebar.multiselect(
    "Brand",
    sorted(df["Brand"].unique()),
    default=sorted(df["Brand"].unique())
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Product_Category"].isin(categories)) &
    (df["Brand"].isin(brands))
]

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

st.subheader("📊 Product KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📦 Products",
    filtered_df["Product_ID"].nunique()
)

col2.metric(
    "🏷️ Brands",
    filtered_df["Brand"].nunique()
)

col3.metric(
    "📂 Categories",
    filtered_df["Product_Category"].nunique()
)

col4.metric(
    "💰 Revenue",
    f"${filtered_df['Revenue'].sum():,.2f}"
)

st.markdown("---")

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "🛒 Units Sold",
    f"{filtered_df['Units_Sold'].sum():,}"
)

col6.metric(
    "💲 Avg Unit Price",
    f"${filtered_df['Unit_Price'].mean():,.2f}"
)

col7.metric(
    "📉 Avg Discount",
    f"{filtered_df['Discount_Percentage'].mean():.2f}%"
)

col8.metric(
    "📦 Avg Stock",
    round(filtered_df["Stock_On_Hand"].mean(),2)
)

st.markdown("---")

# --------------------------------------------------
# Revenue by Product Category
# --------------------------------------------------

st.subheader("📂 Revenue by Category")

category_df = (
    filtered_df
    .groupby("Product_Category")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(by="Revenue", ascending=False)
)

fig = px.bar(
    category_df,
    x="Product_Category",
    y="Revenue",
    color="Revenue",
    text_auto=".2s",
    title="Revenue by Category"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("📁 Revenue by Subcategory")

subcategory_df = (
    filtered_df
    .groupby("Product_Subcategory")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(by="Revenue", ascending=False)
)

fig = px.bar(
    subcategory_df,
    x="Product_Subcategory",
    y="Revenue",
    color="Revenue",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 Top 10 Products")

top_products = (
    filtered_df
    .groupby("Product_ID")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(by="Revenue", ascending=False)
    .head(10)
)

fig = px.bar(
    top_products,
    x="Product_ID",
    y="Revenue",
    color="Revenue",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏷️ Top Brands")

brand_df = (
    filtered_df
    .groupby("Brand")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(by="Revenue", ascending=False)
)

fig = px.bar(
    brand_df,
    x="Brand",
    y="Revenue",
    color="Revenue",
    text_auto=".2s"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🥧 Revenue Share by Category")

fig = px.pie(
    category_df,
    names="Product_Category",
    values="Revenue",
    hole=0.45
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📦 Inventory Analysis")

stock_df = (
    filtered_df
    .groupby("Product_Category")["Stock_On_Hand"]
    .mean()
    .reset_index()
)

fig = px.bar(
    stock_df,
    x="Product_Category",
    y="Stock_On_Hand",
    color="Stock_On_Hand",
    text_auto=".2f"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Product Performance")

product_table = (
    filtered_df
    .groupby(
        [
            "Product_ID",
            "Brand",
            "Product_Category"
        ]
    )
    .agg({
        "Revenue":"sum",
        "Units_Sold":"sum",
        "Stock_On_Hand":"mean"
    })
    .reset_index()
)

st.dataframe(
    product_table,
    use_container_width=True,
    height=400
)

csv = product_table.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Product Report",
    csv,
    "Product_Report.csv",
    "text/csv"
)

st.subheader("💡 Product Insights")

best_category = category_df.iloc[0]

best_brand = brand_df.iloc[0]

st.success(f"""
### Product Summary

🏆 Best Category: **{best_category['Product_Category']}**

💰 Revenue: **${best_category['Revenue']:,.2f}**

🏷️ Best Brand: **{best_brand['Brand']}**

💵 Brand Revenue: **${best_brand['Revenue']:,.2f}**

📦 Products: **{filtered_df['Product_ID'].nunique()}**

🛒 Units Sold: **{filtered_df['Units_Sold'].sum():,}**
""")

