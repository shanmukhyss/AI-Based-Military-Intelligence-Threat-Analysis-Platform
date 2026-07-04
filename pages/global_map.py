import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import add_features

# ----------------------------------------------------------
# Page Config
# ----------------------------------------------------------

st.set_page_config(
    page_title="Global Threat Map",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Threat Map")

st.markdown(
"""
Explore terrorist incidents around the world using interactive filters.
"""
)

st.divider()

# ----------------------------------------------------------
# Load Data
# ----------------------------------------------------------

df = load_data()
df = add_features(df)

# ----------------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------------

st.sidebar.header("🔍 Filters")

years = sorted(df["iyear"].unique())

regions = sorted(df["region_txt"].unique())

countries = sorted(df["country_txt"].unique())

attack_types = sorted(df["attacktype1_txt"].unique())

selected_year = st.sidebar.selectbox(
    "Year",
    ["All"] + years
)

selected_region = st.sidebar.selectbox(
    "Region",
    ["All"] + regions
)

selected_country = st.sidebar.selectbox(
    "Country",
    ["All"] + countries
)

selected_attack = st.sidebar.selectbox(
    "Attack Type",
    ["All"] + attack_types
)

# ----------------------------------------------------------
# Apply Filters
# ----------------------------------------------------------

filtered = df.copy()

if selected_year != "All":
    filtered = filtered[
        filtered["iyear"] == selected_year
    ]

if selected_region != "All":
    filtered = filtered[
        filtered["region_txt"] == selected_region
    ]

if selected_country != "All":
    filtered = filtered[
        filtered["country_txt"] == selected_country
    ]

if selected_attack != "All":
    filtered = filtered[
        filtered["attacktype1_txt"] == selected_attack
    ]

# ----------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Incidents",
    f"{len(filtered):,}"
)

c2.metric(
    "Fatalities",
    f"{int(filtered['nkill'].sum()):,}"
)

c3.metric(
    "Injuries",
    f"{int(filtered['nwound'].sum()):,}"
)

c4.metric(
    "Countries",
    filtered["country_txt"].nunique()
)

st.divider()

# ----------------------------------------------------------
# Interactive World Map
# ----------------------------------------------------------

sample_size = min(10000, len(filtered))

map_df = filtered.sample(
    sample_size,
    random_state=42
)

fig = px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    color="attacktype1_txt",
    hover_name="country_txt",
    hover_data={
        "city": True,
        "region_txt": True,
        "gname": True,
        "attacktype1_txt": False,
        "nkill": True,
        "nwound": True,
        "threat_level": True,
        "latitude": False,
        "longitude": False
    },
    projection="natural earth",
    title="Global Terrorist Incidents"
)

fig.update_layout(
    height=700,
    legend_title="Attack Type",
    margin=dict(
        l=10,
        r=10,
        t=60,
        b=10
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------------
# Bottom Charts
# ----------------------------------------------------------

left, right = st.columns(2)

with left:

    country = (
        filtered["country_txt"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    country.columns = [
        "Country",
        "Attacks"
    ]

    fig = px.bar(
        country,
        x="Country",
        y="Attacks",
        text="Attacks",
        title="Top Affected Countries"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    attack = (
        filtered["attacktype1_txt"]
        .value_counts()
        .reset_index()
    )

    attack.columns = [
        "Attack Type",
        "Count"
    ]

    fig = px.pie(
        attack,
        names="Attack Type",
        values="Count",
        title="Attack Type Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------------------------
# Recent Incidents
# ----------------------------------------------------------

st.divider()

st.subheader("📋 Incident Records")

show_columns = [
    "date",
    "country_txt",
    "city",
    "region_txt",
    "attacktype1_txt",
    "weaptype1_txt",
    "gname",
    "nkill",
    "nwound",
    "threat_level"
]

st.dataframe(
    filtered[show_columns],
    use_container_width=True,
    height=400
)