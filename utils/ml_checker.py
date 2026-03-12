import joblib

model = joblib.load("models/phishing_model.pkl")

def extract_features(url):
    return [
        len(url),
        url.count("-"),
        url.count("."),
        sum(c.isdigit() for c in url)
    ]

def check_ml_phishing(url):
    features = extract_features(url)
    prediction = model.predict([features])[0]

    if prediction == 1:
        return 35, ["ML model predicts phishing behaviour"]
    else:
        return 5, ["ML model predicts safe behaviour"]