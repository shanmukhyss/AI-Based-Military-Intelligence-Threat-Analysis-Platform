import streamlit as st
import pandas as pd
import joblib

from utils.data_loader import load_data

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------

st.set_page_config(
    page_title="Attack Prediction",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Attack Type Prediction")

st.markdown(
"""
Predict the most likely attack type based on location,
target type and weapon type.
"""
)

st.divider()

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

df = load_data()

# ----------------------------------------------------------
# LOAD MODEL
# ----------------------------------------------------------

model = joblib.load("models/attack_model.pkl")

feature_encoders = joblib.load(
    "models/feature_encoders.pkl"
)

target_encoder = joblib.load(
    "models/target_encoder.pkl"
)

# ----------------------------------------------------------
# INPUTS
# ----------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    country = st.selectbox(
        "Country",
        sorted(df["country_txt"].unique())
    )

    region = st.selectbox(
        "Region",
        sorted(df["region_txt"].unique())
    )

with col2:

    target = st.selectbox(
        "Target Type",
        sorted(df["targtype1_txt"].unique())
    )

    weapon = st.selectbox(
        "Weapon Type",
        sorted(df["weaptype1_txt"].unique())
    )

st.divider()

# ----------------------------------------------------------
# PREDICT
# ----------------------------------------------------------

if st.button("Predict Attack Type"):

    input_df = pd.DataFrame({

        "country_txt":[
            feature_encoders["country_txt"].transform([country])[0]
        ],

        "region_txt":[
            feature_encoders["region_txt"].transform([region])[0]
        ],

        "targtype1_txt":[
            feature_encoders["targtype1_txt"].transform([target])[0]
        ],

        "weaptype1_txt":[
            feature_encoders["weaptype1_txt"].transform([weapon])[0]
        ]

    })

    prediction = model.predict(input_df)[0]

    attack = target_encoder.inverse_transform(
        [prediction]
    )[0]

    probabilities = model.predict_proba(input_df)[0]

    confidence = probabilities.max() * 100

    st.success(
        f"Predicted Attack Type : **{attack}**"
    )

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    st.subheader("Class Probabilities")

    probability_df = pd.DataFrame({

        "Attack Type":
            target_encoder.classes_,

        "Probability (%)":
            probabilities * 100

    })

    probability_df = probability_df.sort_values(
        by="Probability (%)",
        ascending=False
    )

    st.dataframe(
        probability_df,
        use_container_width=True
    )