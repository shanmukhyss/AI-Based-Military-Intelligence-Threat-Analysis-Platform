import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

from utils.data_loader import load_data

# ==========================================================
# Load Dataset
# ==========================================================

print("=" * 70)
print("Loading Dataset...")
print("=" * 70)

df = load_data()

# ==========================================================
# Select Features
# ==========================================================

features = [
    "country_txt",
    "region_txt",
    "targtype1_txt",
    "weaptype1_txt"
]

target = "attacktype1_txt"

df = df[features + [target]].copy()

# Remove Unknown attack types
df = df[df[target] != "Unknown"]

# Remove Missing Values
df.dropna(inplace=True)

print(f"Dataset Shape : {df.shape}")

# ==========================================================
# Encode Features
# ==========================================================

feature_encoders = {}

for col in features:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])
    feature_encoders[col] = encoder

# ==========================================================
# Encode Target
# ==========================================================

target_encoder = LabelEncoder()
df[target] = target_encoder.fit_transform(df[target])

# ==========================================================
# Split Dataset
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

print(f"Training Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")

# ==========================================================
# Train Model
# ==========================================================

print("\nTraining Optimized Random Forest...\n")

model = RandomForestClassifier(
    n_estimators=100,
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
# Evaluation
# ==========================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("=" * 70)
print(f"Accuracy : {accuracy:.4f}")
print("=" * 70)

print(classification_report(
    y_test,
    predictions,
    target_names=target_encoder.classes_
))

# ==========================================================
# Save Model
# ==========================================================

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/attack_model.pkl",
    compress=("xz", 3)
)

joblib.dump(
    feature_encoders,
    "models/feature_encoders.pkl"
)

joblib.dump(
    target_encoder,
    "models/target_encoder.pkl"
)

print("\nModel Saved Successfully!")
print("models/attack_model.pkl")
print("models/feature_encoders.pkl")
print("models/target_encoder.pkl")

# ==========================================================
# Show Model Size
# ==========================================================

size_mb = os.path.getsize("models/attack_model.pkl") / (1024 * 1024)

print("=" * 70)
print(f"Model Size : {size_mb:.2f} MB")
print("=" * 70)