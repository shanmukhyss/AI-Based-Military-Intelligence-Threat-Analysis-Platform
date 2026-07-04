import streamlit as st


def page_title(title):

    st.title(title)

    st.divider()


def sidebar_filters(df):

    years = sorted(df["iyear"].unique())

    countries = sorted(df["country_txt"].unique())

    regions = sorted(df["region_txt"].unique())

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

    return year, country, region


def apply_filters(df, year, country, region):

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

    return filtered