import streamlit as st

st.set_page_config(
    page_title="AI Military Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
)

home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠",
)

map_page = st.Page(
    "pages/global_map.py",
    title="Global Threat Map",
    icon="🌍",
)

country = st.Page(
    "pages/country_analysis.py",
    title="Country Analysis",
    icon="📊",
)

attack = st.Page(
    "pages/attack_prediction.py",
    title="Attack Prediction",
    icon="🎯",
)

threat = st.Page(
    "pages/threat_prediction.py",
    title="Threat Level Prediction",
    icon="⚠️",
)

forecast = st.Page(
    "pages/forecasting.py",
    title="Forecasting",
    icon="📈",
)

report = st.Page(
    "pages/ai_report.py",
    title="AI Intelligence Report",
    icon="🧠",
)

explorer = st.Page(
    "pages/data_explorer.py",
    title="Data Explorer",
    icon="🔍",
)

settings = st.Page(
    "pages/settings.py",
    title="Settings",
    icon="⚙️",
)

pg = st.navigation(
    {
        "Main": [home],
        "Analytics": [
            map_page,
            country,
            forecast,
        ],
        "AI Models": [
            attack,
            threat,
            report,
        ],
        "Utilities": [
            explorer,
            settings,
        ],
    }
)

pg.run()