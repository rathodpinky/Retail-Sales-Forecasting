import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_data

st.set_page_config(
    page_title="Business Insights",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Business Insights Dashboard")

st.markdown("---")

df = load_data()

st.subheader("📊 Executive KPIs")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Revenue",
    f"${df['Revenue'].sum():,.2f}"
)

col2.metric(
    "Stores",
    df["Store_ID"].nunique()
)

col3.metric(
    "Products",
    df["Product_ID"].nunique()
)

col4.metric(
    "Brands",
    df["Brand"].nunique()
)

st.markdown("---")

region_df = (
    df.groupby("Region")["Revenue"]
    .sum()
    .reset_index()
)

best_region = region_df.sort_values(
    "Revenue",
    ascending=False
).iloc[0]

st.success(f"""
## 🌍 Best Region

**{best_region['Region']}**

Revenue:

**${best_region['Revenue']:,.2f}**
""")

store_df = (
    df.groupby("Store_ID")["Revenue"]
    .sum()
    .reset_index()
)

best_store = store_df.sort_values(
    "Revenue",
    ascending=False
).iloc[0]

st.success(f"""
## 🏪 Best Store

Store:

**{best_store['Store_ID']}**

Revenue:

**${best_store['Revenue']:,.2f}**
""")


category_df = (
    df.groupby("Product_Category")["Revenue"]
    .sum()
    .reset_index()
)

fig_category = px.bar(
    category_df,
    x="Product_Category",
    y="Revenue",
    color="Revenue",
    text_auto=".2s"
)

st.plotly_chart(
    fig_category,
    use_container_width=True,
    key="category_revenue"
)

brand_df = (
    df.groupby("Brand")["Revenue"]
    .sum()
    .reset_index()
)

fig_brand = px.bar(
    brand_df,
    x="Brand",
    y="Revenue",
    color="Revenue",
    text_auto=".2s"
)

st.plotly_chart(
    fig_brand,
    use_container_width=True,
    key="brand_revenue"
)

promo_df = (
    df.groupby("Promotion_Applied")["Revenue"]
    .sum()
    .reset_index()
)

fig_promo = px.pie(
    promo_df,
    names="Promotion_Applied",
    values="Revenue",
    hole=.45
)

st.plotly_chart(
    fig_promo,
    use_container_width=True,
    key="promo_effect"
)

inventory = (
    df.groupby("Product_Category")["Stock_On_Hand"]
    .mean()
    .reset_index()
)

fig_inventory = px.bar(
    inventory,
    x="Product_Category",
    y="Stock_On_Hand",
    color="Stock_On_Hand",
    text_auto=".2f"
)

st.plotly_chart(
    fig_inventory,
    use_container_width=True,
    key="inventory_risk"
)

rating = (
    df.groupby("Store_ID")["Store_Rating"]
    .mean()
    .reset_index()
)

fig_rating = px.bar(
    rating,
    x="Store_ID",
    y="Store_Rating",
    color="Store_Rating",
    text_auto=".2f"
)

st.plotly_chart(
    fig_rating,
    use_container_width=True,
    key="store_rating"
)

st.subheader("🤖 AI Recommendations")

top_category = (
    category_df.sort_values(
        "Revenue",
        ascending=False
    ).iloc[0]
)

low_stock = inventory.sort_values(
    "Stock_On_Hand"
).iloc[0]

st.info(f"""
### 📈 Business Recommendations

✅ Increase inventory for **{top_category['Product_Category']}**

✅ Focus marketing campaigns in **{best_region['Region']}**

✅ Replicate the sales strategy of **Store {best_store['Store_ID']}**

✅ Review inventory levels for **{low_stock['Product_Category']}**

✅ Increase promotions for low-performing categories.

✅ Maintain high customer satisfaction by improving store ratings.
""")

