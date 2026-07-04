import streamlit as st

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Settings")

st.divider()

st.subheader("Application Information")

st.info(
"""
AI-Based Military Intelligence and Threat Analysis Dashboard

Version : 1.0

Dataset : Global Terrorism Database (GTD)

Records : 181,691

Years Covered : 1970 - 2017

Developed using:

• Streamlit

• Plotly

• Scikit-Learn

• Prophet

• Google Gemini (AI Reports)
"""
)

st.divider()

st.subheader("Model Information")

st.write("Attack Prediction Model : Random Forest")

st.write("Threat Prediction Model : Random Forest")

st.write("Forecasting Model : Facebook Prophet")

st.divider()

st.subheader("Developer")

st.success(
"""
Built using Python, Machine Learning, Data Analytics,
Interactive Visualization and Artificial Intelligence.
"""
)