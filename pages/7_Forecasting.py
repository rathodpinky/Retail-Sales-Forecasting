import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

from utils.load_data import load_data

st.set_page_config(
    page_title="Sales Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Sales Forecasting Dashboard")

st.markdown("---")

df = load_data()

df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("Forecast Settings")

forecast_model = st.sidebar.selectbox(
    "Forecast Model",
    [
        "Prophet",
        "ARIMA"
    ]
)

forecast_days = st.sidebar.selectbox(
    "Forecast Period",
    [
        30,
        90,
        365
    ]
)

forecast = pd.read_csv(
    "data/Revenue_Forecast.csv"
)

forecast["ds"] = pd.to_datetime(
    forecast["ds"]
)

st.subheader("Forecast Summary")

col1,col2,col3,col4 = st.columns(4)

future = forecast.tail(forecast_days)

col1.metric(
    "Forecast Days",
    forecast_days
)

col2.metric(
    "Average Revenue",
    f"${future['yhat'].mean():,.2f}"
)

col3.metric(
    "Maximum Revenue",
    f"${future['yhat'].max():,.2f}"
)

col4.metric(
    "Minimum Revenue",
    f"${future['yhat'].min():,.2f}"
)

st.markdown("---")

st.subheader("Revenue Forecast")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat"],
        name="Forecast",
        line=dict(color="royalblue")
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat_upper"],
        name="Upper",
        line=dict(dash="dot")
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat_lower"],
        name="Lower",
        line=dict(dash="dot"),
        fill="tonexty"
    )
)

fig.update_layout(
    title="Revenue Forecast",
    xaxis_title="Date",
    yaxis_title="Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="forecast_chart"
)


st.subheader("Forecast Data")

st.dataframe(
    future,
    use_container_width=True,
    height=450
)

csv = future.to_csv(index=False).encode()

st.download_button(
    "📥 Download Forecast",
    csv,
    f"{forecast_model}_{forecast_days}_Days.csv",
    "text/csv"
)

st.subheader("Forecast Distribution")

fig_hist = px.histogram(
    future,
    x="yhat",
    nbins=25,
    title="Forecast Revenue Distribution"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True,
    key="forecast_distribution"
)

st.subheader("💡 Forecast Insights")

growth = (
    future["yhat"].iloc[-1] -
    future["yhat"].iloc[0]
)

trend = "Increasing 📈" if growth > 0 else "Decreasing 📉"

st.success(f"""
### AI Forecast Summary

📅 Forecast Period : **{forecast_days} Days**

📈 Revenue Trend : **{trend}**

💰 Expected Average Revenue :
**${future['yhat'].mean():,.2f}**

🚀 Highest Expected Revenue :
**${future['yhat'].max():,.2f}**

📉 Lowest Expected Revenue :
**${future['yhat'].min():,.2f}**
""")

