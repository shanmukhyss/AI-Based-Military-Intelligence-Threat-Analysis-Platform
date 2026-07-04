import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from utils.data_loader import load_data

# ==========================================================
# LOAD DATA
# ==========================================================

print("=" * 70)
print("Loading Dataset...")
print("=" * 70)

df = load_data()

# ==========================================================
# CREATE THREAT SCORE
# ==========================================================

df["threat_score"] = (
    df["nkill"] * 3 +
    df["nwound"] +
    df["property"].clip(lower=0) * 5
)

# ==========================================================
# CREATE THREAT LEVEL
# ==========================================================

def threat_level(score):

    if score <= 5:
        return "Low"

    elif score <= 20:
        return "Medium"

    elif score <= 50:
        return "High"

    return "Critical"

df["threat_level"] = df["threat_score"].apply(threat_level)

# ==========================================================
# FEATURES
# ==========================================================

features = [
    "country_txt",
    "region_txt",
    "attacktype1_txt",
    "targtype1_txt",
    "weaptype1_txt"
]

target = "threat_level"

df = df[features + [target]].copy()

# ==========================================================
# ENCODE FEATURES
# ==========================================================

feature_encoders = {}

for col in features:

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col])

    feature_encoders[col] = encoder

# ==========================================================
# ENCODE TARGET
# ==========================================================

target_encoder = LabelEncoder()

df[target] = target_encoder.fit_transform(df[target])

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

X = df[features]

y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ==========================================================
# MODEL
# ==========================================================

# ==========================================================
# MODEL
# ==========================================================

print("\nTraining Optimized Threat Model...\n")

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features="sqrt",
    bootstrap=True,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ==========================================================
# EVALUATION
# ==========================================================

pred = model.predict(X_test)

acc = accuracy_score(
    y_test,
    pred
)

print("=" * 70)
print(f"Accuracy : {acc:.4f}")
print("=" * 70)

print(classification_report(
    y_test,
    pred,
    target_names=target_encoder.classes_
))

# ==========================================================
# SAVE
# ==========================================================

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/threat_model.pkl",
    compress=("xz", 3)
)

joblib.dump(
    feature_encoders,
    "models/threat_feature_encoders.pkl"
)

joblib.dump(
    target_encoder,
    "models/threat_target_encoder.pkl"
)

print("\nThreat Model Saved Successfully!")