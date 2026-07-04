import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

from dotenv import load_dotenv

from utils.data_loader import load_data
from utils.preprocessing import add_features

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="AI Intelligence Report",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Intelligence Report")

st.markdown(
"""
Generate an AI-powered intelligence assessment from the
Global Terrorism Database.
"""
)

st.divider()

# -------------------------------------------------------
# LOAD API
# -------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:

    st.error(
        "Gemini API Key not found.\nCreate a .env file and add GEMINI_API_KEY."
    )

    st.stop()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

df = load_data()
df = add_features(df)

# -------------------------------------------------------
# FILTERS
# -------------------------------------------------------

countries = sorted(df["country_txt"].unique())

country = st.selectbox(
    "Country",
    countries,
    index=countries.index("India") if "India" in countries else 0
)

year1, year2 = st.slider(
    "Year Range",
    1970,
    2017,
    (2010, 2017)
)

filtered = df[
    (df["country_txt"] == country)
    &
    (df["iyear"] >= year1)
    &
    (df["iyear"] <= year2)
]

# -------------------------------------------------------
# SUMMARY
# -------------------------------------------------------

total = len(filtered)

deaths = int(filtered["nkill"].sum())

injuries = int(filtered["nwound"].sum())

top_attack = (
    filtered["attacktype1_txt"]
    .value_counts()
    .idxmax()
)

top_weapon = (
    filtered["weaptype1_txt"]
    .value_counts()
    .idxmax()
)

groups = (
    filtered[filtered["gname"] != "Unknown"]["gname"]
    .value_counts()
    .head(5)
    .to_dict()
)

st.subheader("Dataset Summary")

st.write(f"Incidents : {total}")
st.write(f"Fatalities : {deaths}")
st.write(f"Injuries : {injuries}")
st.write(f"Most Common Attack : {top_attack}")
st.write(f"Most Common Weapon : {top_weapon}")
st.write(groups)

st.divider()

# -------------------------------------------------------
# PROMPT
# -------------------------------------------------------

if st.button("Generate Intelligence Report"):

    prompt = f"""
You are a Military Intelligence Analyst.

Prepare a professional intelligence report.

Country : {country}

Years : {year1}-{year2}

Total Incidents : {total}

Fatalities : {deaths}

Injuries : {injuries}

Most Common Attack :
{top_attack}

Most Common Weapon :
{top_weapon}

Top Terrorist Groups :
{groups}

The report should contain:

1. Executive Summary

2. Threat Assessment

3. Operational Analysis

4. Emerging Trends

5. Strategic Recommendations

6. Risk Level

Keep it concise and professional.
"""

    with st.spinner("Generating AI Report..."):

        response = model.generate_content(prompt)

    st.subheader("Generated Intelligence Report")

    st.markdown(response.text)