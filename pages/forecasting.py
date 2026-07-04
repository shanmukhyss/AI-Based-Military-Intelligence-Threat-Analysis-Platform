import streamlit as st
import pandas as pd
import plotly.express as px

from prophet import Prophet

from utils.data_loader import load_data

st.set_page_config(
    page_title="Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Terrorism Forecasting")

st.markdown(
"""
Forecast the expected number of terrorist attacks using Facebook Prophet.
"""
)

st.divider()

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

df = load_data()

# -----------------------------------------------------
# PREPARE DATA
# -----------------------------------------------------

forecast_df = (
    df.groupby("date")
      .size()
      .reset_index(name="y")
)

forecast_df.columns = ["ds", "y"]

# Prophet expects columns:
# ds -> Date
# y  -> Value

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

months = st.sidebar.slider(
    "Forecast Months",
    min_value=6,
    max_value=60,
    value=24
)

# -----------------------------------------------------
# TRAIN MODEL
# -----------------------------------------------------

with st.spinner("Training forecasting model..."):

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(forecast_df)

    future = model.make_future_dataframe(
        periods=months * 30
    )

    forecast = model.predict(future)

st.success("Forecast Generated Successfully")

# -----------------------------------------------------
# FORECAST GRAPH
# -----------------------------------------------------

fig = px.line(
    forecast,
    x="ds",
    y="yhat",
    title="Forecasted Terrorist Attacks"
)

fig.add_scatter(
    x=forecast_df["ds"],
    y=forecast_df["y"],
    mode="lines",
    name="Historical"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -----------------------------------------------------
# COMPONENTS
# -----------------------------------------------------

trend = px.line(
    forecast,
    x="ds",
    y="trend",
    title="Trend Component"
)

st.plotly_chart(
    trend,
    use_container_width=True
)

st.divider()

# -----------------------------------------------------
# FORECAST TABLE
# -----------------------------------------------------

table = forecast[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
].tail(months * 30)

table.columns = [
    "Date",
    "Predicted Attacks",
    "Lower Bound",
    "Upper Bound"
]

st.dataframe(
    table,
    use_container_width=True,
    height=400
)

csv = table.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Forecast",
    csv,
    "forecast.csv",
    "text/csv"
)