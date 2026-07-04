import pandas as pd


def get_dashboard_metrics(df):

    metrics = {}

    metrics["total_attacks"] = len(df)

    metrics["total_deaths"] = int(df["nkill"].sum())

    metrics["total_injuries"] = int(df["nwound"].sum())

    metrics["countries"] = df["country_txt"].nunique()

    metrics["success_rate"] = round(
        df["success"].mean() * 100,
        2
    )

    metrics["top_country"] = (
        df["country_txt"]
        .value_counts()
        .idxmax()
    )

    metrics["top_attack"] = (
        df["attacktype1_txt"]
        .value_counts()
        .idxmax()
    )

    groups = df[df["gname"] != "Unknown"]

    metrics["top_group"] = (
        groups["gname"]
        .value_counts()
        .idxmax()
    )

    return metrics


def attacks_per_year(df):

    return (
        df.groupby("iyear")
        .size()
        .reset_index(name="Attacks")
    )


def top_countries(df, n=10):

    return (
        df["country_txt"]
        .value_counts()
        .head(n)
        .reset_index(name="Attacks")
        .rename(columns={"country_txt": "Country"})
    )


def top_attack_types(df):

    return (
        df["attacktype1_txt"]
        .value_counts()
        .reset_index(name="Count")
        .rename(columns={"attacktype1_txt": "Attack Type"})
    )


def top_weapon_types(df):

    weapon = df[df["weaptype1_txt"] != "Unknown"]

    return (
        weapon["weaptype1_txt"]
        .value_counts()
        .head(10)
        .reset_index(name="Count")
        .rename(columns={"weaptype1_txt": "Weapon"})
    )


def top_groups(df):

    groups = df[df["gname"] != "Unknown"]

    return (
        groups["gname"]
        .value_counts()
        .head(15)
        .reset_index(name="Attacks")
        .rename(columns={"gname": "Group"})
    )


def country_statistics(df, country):

    return df[df["country_txt"] == country]