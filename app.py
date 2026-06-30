import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Retail Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Analytics & AI-Powered Sales Forecasting")

st.markdown("""
Welcome to the Retail Analytics Dashboard.

Use the menu on the left to navigate through the different pages.
""")

def load_css():
    with open("assets/custom.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

logo = Image.open("assets/logo.png")

st.sidebar.image(logo, width=180)

st.markdown("""
# 🏪 Retail Sales Forecasting Dashboard

### AI-Powered Retail Analytics

This dashboard provides:

- 📈 Sales Analytics
- 📦 Product Analytics
- 🏪 Store Analytics
- 👥 Customer Analytics
- 🤖 AI Revenue Prediction
- 📅 Sales Forecasting
- 💡 Business Insights
""")

st.markdown("---")

st.caption(
    "Retail Sales Forecasting Dashboard | Built with Streamlit, Plotly & XGBoost"
)