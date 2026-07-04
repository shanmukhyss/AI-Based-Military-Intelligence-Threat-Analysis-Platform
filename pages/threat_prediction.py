import streamlit as st
import pandas as pd
import joblib

from utils.data_loader import load_data

st.set_page_config(
    page_title="Threat Level Prediction",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Threat Level Prediction")

st.markdown(
"""
Predict the expected threat level based on the incident characteristics.
"""
)

st.divider()

df = load_data()

model = joblib.load(
    "models/threat_model.pkl"
)

feature_encoders = joblib.load(
    "models/threat_feature_encoders.pkl"
)

target_encoder = joblib.load(
    "models/threat_target_encoder.pkl"
)

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

    attack = st.selectbox(
        "Attack Type",
        sorted(df["attacktype1_txt"].unique())
    )

    target = st.selectbox(
        "Target Type",
        sorted(df["targtype1_txt"].unique())
    )

weapon = st.selectbox(
    "Weapon Type",
    sorted(df["weaptype1_txt"].unique())
)

st.divider()

if st.button("Predict Threat Level"):

    sample = pd.DataFrame({

        "country_txt":[
            feature_encoders["country_txt"].transform([country])[0]
        ],

        "region_txt":[
            feature_encoders["region_txt"].transform([region])[0]
        ],

        "attacktype1_txt":[
            feature_encoders["attacktype1_txt"].transform([attack])[0]
        ],

        "targtype1_txt":[
            feature_encoders["targtype1_txt"].transform([target])[0]
        ],

        "weaptype1_txt":[
            feature_encoders["weaptype1_txt"].transform([weapon])[0]
        ]

    })

    prediction = model.predict(sample)[0]

    level = target_encoder.inverse_transform(
        [prediction]
    )[0]

    probability = model.predict_proba(sample)[0]

    confidence = probability.max() * 100

    colors = {
        "Low":"🟢",
        "Medium":"🟡",
        "High":"🟠",
        "Critical":"🔴"
    }

    st.success(
        f"Threat Level : {colors[level]} **{level}**"
    )

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    prob_df = pd.DataFrame({

        "Threat Level":
            target_encoder.classes_,

        "Probability (%)":
            probability * 100

    })

    prob_df = prob_df.sort_values(
        "Probability (%)",
        ascending=False
    )

    st.dataframe(
        prob_df,
        use_container_width=True
    )