import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.preprocessing import add_features

st.set_page_config(
    page_title="Data Explorer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Data Explorer")

st.markdown(
"""
Explore and filter the Global Terrorism Database.
"""
)

st.divider()

# --------------------------------------------------------
# Load Data
# --------------------------------------------------------

df = load_data()
df = add_features(df)

# --------------------------------------------------------
# Sidebar Filters
# --------------------------------------------------------

st.sidebar.header("Filters")

years = sorted(df["iyear"].unique())

countries = sorted(df["country_txt"].unique())

regions = sorted(df["region_txt"].unique())

attacks = sorted(df["attacktype1_txt"].unique())

weapons = sorted(df["weaptype1_txt"].unique())

year = st.sidebar.selectbox(
    "Year",
    ["All"] + years
)

country = st.sidebar.selectbox(
    "Country",
    ["All"] + countries
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + regions
)

attack = st.sidebar.selectbox(
    "Attack Type",
    ["All"] + attacks
)

weapon = st.sidebar.selectbox(
    "Weapon",
    ["All"] + weapons
)

# --------------------------------------------------------
# Apply Filters
# --------------------------------------------------------

filtered = df.copy()

if year != "All":
    filtered = filtered[
        filtered["iyear"] == year
    ]

if country != "All":
    filtered = filtered[
        filtered["country_txt"] == country
    ]

if region != "All":
    filtered = filtered[
        filtered["region_txt"] == region
    ]

if attack != "All":
    filtered = filtered[
        filtered["attacktype1_txt"] == attack
    ]

if weapon != "All":
    filtered = filtered[
        filtered["weaptype1_txt"] == weapon
    ]

# --------------------------------------------------------
# Search
# --------------------------------------------------------

keyword = st.text_input(
    "Search Terrorist Group"
)

if keyword:

    filtered = filtered[
        filtered["gname"]
        .str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

# --------------------------------------------------------
# KPIs
# --------------------------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Records",
    len(filtered)
)

c2.metric(
    "Fatalities",
    int(filtered["nkill"].sum())
)

c3.metric(
    "Countries",
    filtered["country_txt"].nunique()
)

st.divider()

# --------------------------------------------------------
# Columns
# --------------------------------------------------------

columns = st.multiselect(
    "Choose Columns",
    filtered.columns.tolist(),
    default=[
        "date",
        "country_txt",
        "city",
        "attacktype1_txt",
        "weaptype1_txt",
        "gname",
        "nkill",
        "nwound",
        "threat_level"
    ]
)

st.dataframe(
    filtered[columns],
    use_container_width=True,
    height=600
)

st.divider()

# --------------------------------------------------------
# Download
# --------------------------------------------------------

csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    csv,
    file_name="filtered_dataset.csv",
    mime="text/csv"
)