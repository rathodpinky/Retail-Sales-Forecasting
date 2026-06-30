import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_data

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Customer Analytics Dashboard")
st.markdown("---")

# Load Data
df = load_data()

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------

st.sidebar.header("👥 Customer Filters")

customer_types = st.sidebar.multiselect(
    "Customer Type",
    sorted(df["Customer_Type"].unique()),
    default=sorted(df["Customer_Type"].unique())
)

payment_modes = st.sidebar.multiselect(
    "Payment Mode",
    sorted(df["Payment_Mode"].unique()),
    default=sorted(df["Payment_Mode"].unique())
)

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

filtered_df = df[
    (df["Customer_Type"].isin(customer_types)) &
    (df["Payment_Mode"].isin(payment_modes)) &
    (df["Region"].isin(regions))
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

st.subheader("📊 Customer KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Revenue",
    f"${filtered_df['Revenue'].sum():,.2f}"
)

col2.metric(
    "🛒 Total Sales",
    f"${filtered_df['Total_Sales'].sum():,.2f}"
)

col3.metric(
    "📦 Units Sold",
    f"{filtered_df['Units_Sold'].sum():,}"
)

col4.metric(
    "👥 Customer Types",
    filtered_df["Customer_Type"].nunique()
)

st.markdown("---")

promotion_rate = (
    filtered_df["Promotion_Applied"]
    .eq("Yes")
    .mean() * 100
)

holiday_rate = (
    filtered_df["Holiday_Flag"]
    .eq(1)
    .mean() * 100
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "💵 Avg Revenue",
    f"${filtered_df['Revenue'].mean():,.2f}"
)

col6.metric(
    "🏷 Avg Discount",
    f"{filtered_df['Discount_Percentage'].mean():.2f}%"
)

col7.metric(
    "🎁 Promotion %",
    f"{promotion_rate:.2f}%"
)

col8.metric(
    "🎉 Holiday %",
    f"{holiday_rate:.2f}%"
)

st.markdown("---")

st.subheader("👥 Revenue by Customer Type")

customer_df = (
    filtered_df
    .groupby("Customer_Type")["Revenue"]
    .sum()
    .reset_index()
)

fig_customer = px.bar(
    customer_df,
    x="Customer_Type",
    y="Revenue",
    color="Revenue",
    text_auto=".2s",
    title="Revenue by Customer Type"
)

st.plotly_chart(
    fig_customer,
    use_container_width=True,
    key="customer_revenue"
)

st.subheader("🥧 Customer Type Distribution")

distribution_df = (
    filtered_df["Customer_Type"]
    .value_counts()
    .reset_index()
)

distribution_df.columns = ["Customer_Type", "Count"]

fig_distribution = px.pie(
    distribution_df,
    names="Customer_Type",
    values="Count",
    hole=0.45
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True,
    key="customer_distribution"
)

st.subheader("💳 Revenue by Payment Mode")

payment_df = (
    filtered_df
    .groupby("Payment_Mode")["Revenue"]
    .sum()
    .reset_index()
)

fig_payment = px.bar(
    payment_df,
    x="Payment_Mode",
    y="Revenue",
    color="Revenue",
    text_auto=".2s"
)

st.plotly_chart(
    fig_payment,
    use_container_width=True,
    key="payment_mode"
)

st.subheader("🎁 Promotion Impact")

promo_df = (
    filtered_df
    .groupby("Promotion_Applied")["Revenue"]
    .sum()
    .reset_index()
)

fig_promo = px.pie(
    promo_df,
    names="Promotion_Applied",
    values="Revenue",
    hole=0.45
)

st.plotly_chart(
    fig_promo,
    use_container_width=True,
    key="promotion_analysis"
)

st.subheader("🎉 Holiday vs Non-Holiday Sales")

holiday_df = (
    filtered_df
    .groupby("Holiday_Flag")["Revenue"]
    .sum()
    .reset_index()
)

holiday_df["Holiday_Flag"] = holiday_df["Holiday_Flag"].replace({
    0: "Non-Holiday",
    1: "Holiday"
})

fig_holiday = px.bar(
    holiday_df,
    x="Holiday_Flag",
    y="Revenue",
    color="Revenue",
    text_auto=".2s"
)

st.plotly_chart(
    fig_holiday,
    use_container_width=True,
    key="holiday_sales"
)

st.subheader("💸 Discount Distribution")

fig_discount = px.histogram(
    filtered_df,
    x="Discount_Percentage",
    nbins=25,
    title="Discount Distribution"
)

st.plotly_chart(
    fig_discount,
    use_container_width=True,
    key="discount_distribution"
)

st.subheader("📋 Customer Summary")

summary = (
    filtered_df
    .groupby(
        ["Customer_Type", "Payment_Mode"]
    )
    .agg({
        "Revenue": "sum",
        "Units_Sold": "sum",
        "Discount_Percentage": "mean"
    })
    .reset_index()
)

st.dataframe(
    summary,
    use_container_width=True,
    height=400
)

csv = summary.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Customer Report",
    csv,
    "Customer_Report.csv",
    "text/csv"
)

st.subheader("💡 Customer Insights")

top_customer = customer_df.sort_values(
    "Revenue",
    ascending=False
).iloc[0]

top_payment = payment_df.sort_values(
    "Revenue",
    ascending=False
).iloc[0]

st.success(f"""
### Customer Performance Summary

👥 **Top Customer Type:** {top_customer['Customer_Type']}

💰 **Revenue:** ${top_customer['Revenue']:,.2f}

💳 **Most Preferred Payment Mode:** {top_payment['Payment_Mode']}

💵 **Payment Revenue:** ${top_payment['Revenue']:,.2f}

🎁 **Promotion Usage:** {promotion_rate:.2f}%

🎉 **Holiday Sales:** {holiday_rate:.2f}%
""")

