import os

import kagglehub
import pandas as pd
import streamlit as st
from dotenv import load_dotenv


@st.cache_data
def load_data():
    """
    Loads and preprocesses the Global Terrorism Dataset.
    Works both locally (.env) and on Streamlit Cloud (Secrets).
    """

    # Load .env (does nothing on Streamlit Cloud)
    load_dotenv()

    # Get Kaggle credentials
    username = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_KEY")

    # If running on Streamlit Cloud, use Secrets
    if not username or not key:
        username = st.secrets["KAGGLE_USERNAME"]
        key = st.secrets["KAGGLE_KEY"]

    # Set environment variables for KaggleHub
    os.environ["KAGGLE_USERNAME"] = username
    os.environ["KAGGLE_KEY"] = key

    # Download dataset (cached after first download)
    dataset_path = kagglehub.dataset_download("START-UMD/gtd")

    # Path to CSV
    csv_path = os.path.join(dataset_path, "globalterrorismdb_0718dist.csv")

    # Load dataset
    df = pd.read_csv(
        csv_path,
        encoding="latin1",
        low_memory=False,
    )

    # Keep only required columns
    required_columns = [
        "eventid",
        "iyear",
        "imonth",
        "iday",
        "country_txt",
        "region_txt",
        "city",
        "latitude",
        "longitude",
        "attacktype1_txt",
        "targtype1_txt",
        "weaptype1_txt",
        "gname",
        "success",
        "nkill",
        "nwound",
        "property",
        "summary",
    ]

    df = df[required_columns]

    # Fill missing values
    df["city"] = df["city"].fillna("Unknown")
    df["summary"] = df["summary"].fillna("No Summary")
    df["latitude"] = df["latitude"].fillna(0)
    df["longitude"] = df["longitude"].fillna(0)
    df["nkill"] = df["nkill"].fillna(0)
    df["nwound"] = df["nwound"].fillna(0)

    # Replace unknown month/day
    df["imonth"] = df["imonth"].replace(0, 1)
    df["iday"] = df["iday"].replace(0, 1)

    # Create date column
    df["date"] = pd.to_datetime(
        {
            "year": df["iyear"],
            "month": df["imonth"],
            "day": df["iday"],
        }
    )

    return df