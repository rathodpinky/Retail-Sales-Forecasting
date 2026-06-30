import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_data

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="Store Analytics",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 Store Analytics Dashboard")

st.markdown("---")

df = load_data()

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.header("🏪 Store Filters")

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

locations = st.sidebar.multiselect(
    "Store Location",
    sorted(df["Store_Location"].unique()),
    default=sorted(df["Store_Location"].unique())
)

stores = st.sidebar.multiselect(
    "Store ID",
    sorted(df["Store_ID"].unique()),
    default=sorted(df["Store_ID"].unique())
)

filtered_df = df[
    (df["Region"].isin(regions))
    &
    (df["Store_Location"].isin(locations))
    &
    (df["Store_ID"].isin(stores))
]


st.subheader("📊 Store KPIs")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "🏪 Stores",
    filtered_df["Store_ID"].nunique()
)

col2.metric(
    "💰 Revenue",
    f"${filtered_df['Revenue'].sum():,.2f}"
)

col3.metric(
    "⭐ Avg Rating",
    round(filtered_df["Store_Rating"].mean(),2)
)

col4.metric(
    "📦 Units Sold",
    f"{filtered_df['Units_Sold'].sum():,}"
)

st.markdown("---")

col5,col6,col7,col8 = st.columns(4)

avg_rev = filtered_df.groupby("Store_ID")["Revenue"].sum().mean()

col5.metric(
    "💵 Avg Revenue / Store",
    f"${avg_rev:,.2f}"
)

col6.metric(
    "📦 Avg Stock",
    round(filtered_df["Stock_On_Hand"].mean(),2)
)

col7.metric(
    "🌍 Regions",
    filtered_df["Region"].nunique()
)

col8.metric(
    "📍 Locations",
    filtered_df["Store_Location"].nunique()
)

st.markdown("---")

st.subheader("🏪 Revenue by Store")

store_rev = (
    filtered_df
    .groupby("Store_ID")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(by="Revenue",ascending=False)
)

fig = px.bar(
    store_rev,
    x="Store_ID",
    y="Revenue",
    color="Revenue",
    text_auto=".2s"
)
st.plotly_chart(
    fig,
    use_container_width=True,
    key="store_revenue_chart"
)

left,right = st.columns(2)

top10 = store_rev.head(10)

bottom10 = store_rev.tail(10)

with left:

    st.subheader("🏆 Top Stores")

    fig = px.bar(
        top10,
        x="Store_ID",
        y="Revenue",
        color="Revenue"
    )

    st.plotly_chart(
    fig,
    use_container_width=True,
    key="top_store_chart"
)

with right:

    st.subheader("📉 Bottom Stores")

    fig = px.bar(
        bottom10,
        x="Store_ID",
        y="Revenue",
        color="Revenue"
    )

    st.plotly_chart(
    fig,
    use_container_width=True,
    key="bottom_store_chart"
)


st.subheader("🌍 Revenue by Region")

region_df = (
    filtered_df
    .groupby("Region")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_df,
    names="Region",
    values="Revenue",
    hole=.45
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="region_chart"
)

st.subheader("⭐ Store Ratings")

rating_df = (
    filtered_df
    .groupby("Store_ID")["Store_Rating"]
    .mean()
    .reset_index()
)

fig = px.bar(
    rating_df,
    x="Store_ID",
    y="Store_Rating",
    color="Store_Rating",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="rating_chart"
)

st.subheader("🌍 Average Rating by Region")

region_rating = (
    filtered_df
    .groupby("Region")["Store_Rating"]
    .mean()
    .reset_index()
)

fig = px.bar(
    region_rating,
    x="Region",
    y="Store_Rating",
    color="Store_Rating",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="region_rating_chart"
)

st.subheader("📦 Store Inventory")

inventory = (
    filtered_df
    .groupby("Store_ID")["Stock_On_Hand"]
    .mean()
    .reset_index()
)

fig = px.bar(
    inventory,
    x="Store_ID",
    y="Stock_On_Hand",
    color="Stock_On_Hand",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="inventory_chart"
)

st.subheader("📋 Store Performance")

table = (
    filtered_df
    .groupby(
        [
            "Store_ID",
            "Store_Location",
            "Region"
        ]
    )
    .agg({
        "Revenue":"sum",
        "Units_Sold":"sum",
        "Store_Rating":"mean",
        "Stock_On_Hand":"mean"
    })
    .reset_index()
)

st.dataframe(
    table,
    use_container_width=True,
    height=450
)

csv = table.to_csv(index=False).encode()

st.download_button(
    "📥 Download Store Report",
    csv,
    "Store_Report.csv",
    "text/csv"
)

st.subheader("💡 Store Insights")

top_store = store_rev.iloc[0]

best_region = region_df.sort_values(
    "Revenue",
    ascending=False
).iloc[0]

st.success(f"""
### Store Performance Summary

🏆 Best Store : **{top_store['Store_ID']}**

💰 Revenue : **${top_store['Revenue']:,.2f}**

🌍 Best Region : **{best_region['Region']}**

💵 Region Revenue : **${best_region['Revenue']:,.2f}**

⭐ Average Rating : **{filtered_df['Store_Rating'].mean():.2f}**

🏪 Total Stores : **{filtered_df['Store_ID'].nunique()}**
""")

