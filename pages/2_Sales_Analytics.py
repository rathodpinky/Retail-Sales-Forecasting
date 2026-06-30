import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_data

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales Analytics Dashboard")

st.markdown("---")

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

df = load_data()

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.header("🔍 Filters")

# Date Filter

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region Filter

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

# Product Category Filter

categories = st.sidebar.multiselect(
    "Select Product Category",
    options=sorted(df["Product_Category"].unique()),
    default=sorted(df["Product_Category"].unique())
)

# Store Filter

stores = st.sidebar.multiselect(
    "Select Store",
    options=sorted(df["Store_ID"].unique()),
    default=sorted(df["Store_ID"].unique())
)

# -------------------------------------------------
# Apply Filters
# -------------------------------------------------

filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["Date"] <= pd.to_datetime(date_range[1]))
    ]

filtered_df = filtered_df[
    filtered_df["Region"].isin(regions)
]

filtered_df = filtered_df[
    filtered_df["Product_Category"].isin(categories)
]

filtered_df = filtered_df[
    filtered_df["Store_ID"].isin(stores)
]

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Revenue",
    f"${filtered_df['Revenue'].sum():,.2f}"
)

col2.metric(
    "🛒 Sales",
    f"${filtered_df['Total_Sales'].sum():,.2f}"
)

col3.metric(
    "📦 Units Sold",
    f"{filtered_df['Units_Sold'].sum():,}"
)

col4.metric(
    "🏪 Stores",
    filtered_df["Store_ID"].nunique()
)

st.markdown("---")

# -------------------------------------------------
# Additional KPIs
# -------------------------------------------------

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "⭐ Avg Store Rating",
    round(filtered_df["Store_Rating"].mean(),2)
)

col6.metric(
    "🏷 Avg Discount %",
    f"{filtered_df['Discount_Percentage'].mean():.2f}%"
)

col7.metric(
    "📈 Avg Revenue",
    f"${filtered_df['Revenue'].mean():,.2f}"
)

col8.metric(
    "📍 Regions",
    filtered_df["Region"].nunique()
)

st.markdown("---")

# -------------------------------------------------
# Download Filtered Dataset
# -------------------------------------------------

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="Filtered_Sales_Data.csv",
    mime="text/csv"
)

st.markdown("---")

# =====================================================
# Monthly Revenue Trend
# =====================================================

st.subheader("📈 Monthly Revenue Trend")

monthly = (
    filtered_df
    .groupby(filtered_df["Date"].dt.to_period("M"))["Revenue"]
    .sum()
    .reset_index()
)

monthly["Date"] = monthly["Date"].astype(str)

fig_month = px.line(
    monthly,
    x="Date",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

fig_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue",
    hovermode="x unified"
)

st.plotly_chart(fig_month, use_container_width=True)

# =====================================================
# Daily Revenue Trend
# =====================================================

st.subheader("📅 Daily Revenue Trend")

daily = (
    filtered_df
    .groupby("Date")["Revenue"]
    .sum()
    .reset_index()
)

fig_daily = px.line(
    daily,
    x="Date",
    y="Revenue",
    title="Daily Revenue Trend"
)

fig_daily.update_layout(
    hovermode="x unified"
)

st.plotly_chart(fig_daily, use_container_width=True)

# =====================================================
# Quarterly Revenue
# =====================================================

st.subheader("📊 Quarterly Revenue")

quarter = (
    filtered_df
    .groupby(filtered_df["Date"].dt.to_period("Q"))["Revenue"]
    .sum()
    .reset_index()
)

quarter["Quarter"] = quarter["Date"].astype(str)

fig_quarter = px.bar(
    quarter,
    x="Quarter",
    y="Revenue",
    text_auto=".2s",
    color="Revenue",
    title="Quarter-wise Revenue"
)

st.plotly_chart(fig_quarter, use_container_width=True)

# =====================================================
# Yearly Revenue
# =====================================================

st.subheader("📆 Yearly Revenue")

yearly = (
    filtered_df
    .groupby(filtered_df["Date"].dt.year)["Revenue"]
    .sum()
    .reset_index()
)

yearly.columns = ["Year", "Revenue"]

fig_year = px.bar(
    yearly,
    x="Year",
    y="Revenue",
    text_auto=".2s",
    color="Revenue",
    title="Year-wise Revenue"
)

st.plotly_chart(fig_year, use_container_width=True)

# =====================================================
# Revenue by Region
# =====================================================

st.subheader("🌍 Revenue by Region")

region_df = (
    filtered_df
    .groupby("Region")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(by="Revenue", ascending=False)
)

fig_region = px.bar(
    region_df,
    x="Region",
    y="Revenue",
    color="Revenue",
    text_auto=".2s",
    title="Revenue by Region"
)

fig_region.update_layout(
    xaxis_title="Region",
    yaxis_title="Revenue"
)

st.plotly_chart(fig_region, use_container_width=True)

# =====================================================
# Revenue by Store
# =====================================================

st.subheader("🏪 Revenue by Store")

store_df = (
    filtered_df
    .groupby("Store_ID")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(by="Revenue", ascending=False)
)

fig_store = px.bar(
    store_df,
    x="Store_ID",
    y="Revenue",
    color="Revenue",
    text_auto=".2s",
    title="Revenue by Store"
)

st.plotly_chart(fig_store, use_container_width=True)

# =====================================================
# Top 10 Stores
# =====================================================

st.subheader("🏆 Top 10 Stores")

top10 = store_df.head(10)

fig_top = px.bar(
    top10,
    x="Store_ID",
    y="Revenue",
    color="Revenue",
    text_auto=".2s",
    title="Top 10 Stores"
)

st.plotly_chart(fig_top, use_container_width=True)


# =====================================================
# Monthly Revenue Heatmap
# =====================================================

st.subheader("📊 Revenue Heatmap")

heatmap_df = filtered_df.copy()

heatmap_df["Year"] = heatmap_df["Date"].dt.year
heatmap_df["Month"] = heatmap_df["Date"].dt.month_name()

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

heatmap_df["Month"] = pd.Categorical(
    heatmap_df["Month"],
    categories=month_order,
    ordered=True
)

heat = (
    heatmap_df
    .groupby(["Year","Month"])["Revenue"]
    .sum()
    .reset_index()
)

heat = heat.pivot(
    index="Month",
    columns="Year",
    values="Revenue"
)

fig_heat = px.imshow(
    heat,
    text_auto=".2s",
    aspect="auto",
    title="Revenue Heatmap"
)

st.plotly_chart(fig_heat, use_container_width=True)

# =====================================================
# Sales Data
# =====================================================

st.subheader("📋 Filtered Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

# =====================================================
# Download Excel
# =====================================================

from io import BytesIO

buffer = BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    filtered_df.to_excel(writer, index=False)

st.download_button(
    label="📥 Download Excel Report",
    data=buffer.getvalue(),
    file_name="Sales_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =====================================================
# Business Insights
# =====================================================

st.subheader("💡 Sales Insights")

top_region = region_df.iloc[0]["Region"]
top_region_rev = region_df.iloc[0]["Revenue"]

top_store = store_df.iloc[0]["Store_ID"]
top_store_rev = store_df.iloc[0]["Revenue"]

st.success(f"""
### Key Insights

- 🌍 **Top Performing Region:** {top_region}

- 💰 **Revenue Generated:** ${top_region_rev:,.2f}

- 🏪 **Top Performing Store:** {top_store}

- 💵 **Store Revenue:** ${top_store_rev:,.2f}

- 📦 **Total Units Sold:** {filtered_df['Units_Sold'].sum():,}

- ⭐ **Average Store Rating:** {filtered_df['Store_Rating'].mean():.2f}
""")