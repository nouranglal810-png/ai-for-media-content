import joblib
from utils.trusted_domains import is_domain_trusted

model = joblib.load("models/phishing_model.pkl")

def extract_features(url):
    return [
        len(url),
        url.count("-"),
        url.count("."),
        sum(c.isdigit() for c in url)
    ]

def check_ml_phishing(url):
    # If the domain is a known trusted one, skip ML prediction
    if is_domain_trusted(url):
        return 0, ["ML: Known trusted domain"]

    features = extract_features(url)

    try:
        prediction = model.predict([features])[0]
        proba = model.predict_proba([features])[0]
        confidence = max(proba) * 100

        if prediction == 1:
            # Scale score based on confidence
            if confidence > 80:
                return 30, [f"ML model predicts phishing (confidence: {confidence:.0f}%)"]
            elif confidence > 60:
                return 15, [f"ML model suspects phishing (confidence: {confidence:.0f}%)"]
            else:
                return 5, [f"ML model has low-confidence phishing signal ({confidence:.0f}%)"]
        else:
            return 0, [f"ML model predicts safe (confidence: {confidence:.0f}%)"]
    except:
        return 5, ["ML model prediction unavailable"]