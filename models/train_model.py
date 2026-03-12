import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import re

# sample training dataset
data = {
    "url":[
        "google.com","facebook.com","amazon.com",
        "paypal-login.xyz","secure-bank-login.top",
        "free-money.click","verify-account.tk",
        "netflix.com","instagram.com",
        "update-password.ml"
    ],
    "label":[0,0,0,1,1,1,1,0,0,1]  # 1 = phishing
}

df = pd.DataFrame(data)

def extract_features(url):
    return [
        len(url),
        url.count("-"),
        url.count("."),
        sum(c.isdigit() for c in url)
    ]

X = df["url"].apply(extract_features).tolist()
y = df["label"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train,y_train)

joblib.dump(model,"models/phishing_model.pkl")
print("Model trained and saved!")