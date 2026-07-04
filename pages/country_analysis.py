import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.preprocessing import add_features

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------

st.set_page_config(
    page_title="Country Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Country Analysis")

st.markdown(
"""
Analyze terrorism trends, attack patterns, fatalities,
weapons, targets and terrorist organizations for a selected country.
"""
)

st.divider()

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

df = load_data()
df = add_features(df)

# ----------------------------------------------------------
# COUNTRY SELECTION
# ----------------------------------------------------------

countries = sorted(df["country_txt"].unique())

selected_country = st.selectbox(
    "🌍 Select Country",
    countries,
    index=countries.index("India") if "India" in countries else 0
)

country_df = df[df["country_txt"] == selected_country]

# ----------------------------------------------------------
# KPI CARDS
# ----------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Attacks",
    len(country_df)
)

c2.metric(
    "Fatalities",
    int(country_df["nkill"].sum())
)

c3.metric(
    "Injuries",
    int(country_df["nwound"].sum())
)

c4.metric(
    "Success Rate",
    f"{country_df['success'].mean()*100:.2f}%"
)

st.divider()

# ----------------------------------------------------------
# ATTACKS OVER YEARS
# ----------------------------------------------------------

yearly = (
    country_df.groupby("iyear")
    .size()
    .reset_index(name="Attacks")
)

fig = px.line(
    yearly,
    x="iyear",
    y="Attacks",
    markers=True,
    title=f"Attacks in {selected_country}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------------
# TOP WEAPONS
# ----------------------------------------------------------

left, right = st.columns(2)

with left:

    weapon = (
        country_df[
            country_df["weaptype1_txt"] != "Unknown"
        ]["weaptype1_txt"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    weapon.columns = [
        "Weapon",
        "Count"
    ]

    fig = px.bar(
        weapon,
        x="Weapon",
        y="Count",
        text="Count",
        title="Most Used Weapons"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    attack = (
        country_df["attacktype1_txt"]
        .value_counts()
        .reset_index()
    )

    attack.columns = [
        "Attack",
        "Count"
    ]

    fig = px.pie(
        attack,
        names="Attack",
        values="Count",
        title="Attack Type Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------------
# TARGETS VS GROUPS
# ----------------------------------------------------------

left, right = st.columns(2)

with left:

    target = (
        country_df["targtype1_txt"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    target.columns = [
        "Target",
        "Count"
    ]

    fig = px.bar(
        target,
        x="Target",
        y="Count",
        text="Count",
        title="Top Target Categories"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    groups = (
        country_df[
            country_df["gname"] != "Unknown"
        ]["gname"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    groups.columns = [
        "Group",
        "Attacks"
    ]

    fig = px.bar(
        groups,
        x="Group",
        y="Attacks",
        text="Attacks",
        title="Most Active Terrorist Groups"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------------
# COUNTRY MAP
# ----------------------------------------------------------

st.subheader("🗺️ Incident Locations")

sample = country_df.sample(
    min(3000, len(country_df)),
    random_state=42
)

fig = px.scatter_mapbox(
    sample,
    lat="latitude",
    lon="longitude",
    hover_name="city",
    hover_data=[
        "attacktype1_txt",
        "gname",
        "nkill"
    ],
    color="attacktype1_txt",
    zoom=4,
    height=650
)

fig.update_layout(
    mapbox_style="carto-darkmatter",
    margin=dict(
        l=0,
        r=0,
        t=0,
        b=0
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------------
# THREAT LEVEL
# ----------------------------------------------------------

st.subheader("⚠ Threat Level Distribution")

threat = (
    country_df["threat_level"]
    .value_counts()
    .reset_index()
)

threat.columns = [
    "Threat",
    "Count"
]

fig = px.bar(
    threat,
    x="Threat",
    y="Count",
    color="Threat",
    text="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------------
# INCIDENT TABLE
# ----------------------------------------------------------

st.subheader("📋 Incident Records")

show = [
    "date",
    "city",
    "attacktype1_txt",
    "weaptype1_txt",
    "gname",
    "nkill",
    "nwound",
    "threat_level"
]

st.dataframe(
    country_df[show],
    use_container_width=True,
    height=400
)