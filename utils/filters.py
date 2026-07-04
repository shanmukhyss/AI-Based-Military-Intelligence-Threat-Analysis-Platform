import streamlit as st


def global_filters(df):

    years = sorted(df["iyear"].unique())

    regions = sorted(df["region_txt"].unique())

    countries = sorted(df["country_txt"].unique())

    attacks = sorted(df["attacktype1_txt"].unique())

    st.sidebar.header("Filters")

    year = st.sidebar.selectbox(
        "Year",
        ["All"] + years,
    )

    region = st.sidebar.selectbox(
        "Region",
        ["All"] + regions,
    )

    country = st.sidebar.selectbox(
        "Country",
        ["All"] + countries,
    )

    attack = st.sidebar.selectbox(
        "Attack Type",
        ["All"] + attacks,
    )

    return year, region, country, attack


def apply_filters(df, year, region, country, attack):

    if year != "All":
        df = df[df["iyear"] == year]

    if region != "All":
        df = df[df["region_txt"] == region]

    if country != "All":
        df = df[df["country_txt"] == country]

    if attack != "All":
        df = df[df["attacktype1_txt"] == attack]

    return df