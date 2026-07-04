import pandas as pd


def clean_data(df):
    """
    Basic preprocessing for dashboard.
    """

    df = df.copy()

    df["city"] = df["city"].fillna("Unknown")
    df["summary"] = df["summary"].fillna("No Summary")
    df["latitude"] = df["latitude"].fillna(0)
    df["longitude"] = df["longitude"].fillna(0)
    df["nkill"] = df["nkill"].fillna(0)
    df["nwound"] = df["nwound"].fillna(0)

    return df


def add_features(df):
    """
    Create additional features.
    """

    df = df.copy()

    # Threat Score
    df["threat_score"] = (
        df["nkill"] * 3 +
        df["nwound"] +
        df["property"].clip(lower=0) * 5
    )

    # Threat Level
    def level(score):

        if score <= 5:
            return "Low"

        elif score <= 20:
            return "Medium"

        elif score <= 50:
            return "High"

        return "Critical"

    df["threat_level"] = df["threat_score"].apply(level)

    return df