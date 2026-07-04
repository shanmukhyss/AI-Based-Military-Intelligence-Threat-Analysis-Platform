import plotly.express as px


def yearly_chart(df):

    yearly = (
        df.groupby("iyear")
        .size()
        .reset_index(name="Attacks")
    )

    fig = px.line(
        yearly,
        x="iyear",
        y="Attacks",
        markers=True,
        title="Attacks Over Time"
    )

    return fig


def top_country_chart(df):

    country = (
        df["country_txt"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    country.columns = ["Country", "Attacks"]

    fig = px.bar(
        country,
        x="Country",
        y="Attacks",
        text="Attacks",
        title="Top Countries"
    )

    return fig


def attack_type_chart(df):

    attack = (
        df["attacktype1_txt"]
        .value_counts()
        .reset_index()
    )

    attack.columns = ["Attack", "Count"]

    fig = px.bar(
        attack,
        x="Attack",
        y="Count",
        text="Count",
        title="Attack Types"
    )

    return fig