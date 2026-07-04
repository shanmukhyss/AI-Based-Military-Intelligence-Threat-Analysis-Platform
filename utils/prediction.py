import joblib


class ThreatPredictor:

    def __init__(self):

        self.model = None

        self.encoder = None

    def load(self):

        self.model = joblib.load(
            "models/threat_model.pkl"
        )

        self.encoder = joblib.load(
            "models/feature_encoders.pkl"
        )

    def predict(self, features):

        return self.model.predict(features)