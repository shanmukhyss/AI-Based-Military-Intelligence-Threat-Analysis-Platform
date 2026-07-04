import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import add_features
from utils.analytics import *

st.set_page_config(layout="wide")

df = load_data()
df = add_features(df)

metrics = get_dashboard_metrics(df)

st.title("🏠 Dashboard Overview")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Attacks",
    f"{metrics['total_attacks']:,}"
)

col2.metric(
    "Total Fatalities",
    f"{metrics['total_deaths']:,}"
)

col3.metric(
    "Countries",
    metrics["countries"]
)

col4.metric(
    "Success Rate",
    f"{metrics['success_rate']}%"
)

st.markdown("---")

col5, col6, col7 = st.columns(3)

col5.metric(
    "Top Country",
    metrics["top_country"]
)

col6.metric(
    "Top Attack Type",
    metrics["top_attack"]
)

col7.metric(
    "Top Terrorist Group",
    metrics["top_group"]
)

st.markdown("---")

left, right = st.columns(2)

with left:

    yearly = attacks_per_year(df)

    fig = px.line(
        yearly,
        x="iyear",
        y="Attacks",
        title="Attacks Per Year",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    countries = top_countries(df)

    fig = px.bar(
        countries,
        x="Country",
        y="Attacks",
        title="Top 10 Countries",
        text="Attacks"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

left, right = st.columns(2)

with left:

    attacks = top_attack_types(df)

    fig = px.bar(
        attacks,
        x="Attack Type",
        y="Count",
        title="Attack Types",
        text="Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    groups = top_groups(df)

    fig = px.bar(
        groups,
        x="Group",
        y="Attacks",
        title="Top Terrorist Groups",
        text="Attacks"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )