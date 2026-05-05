# =============================================
# FAST & LIGHTWEIGHT URL CLASSIFIER - COLAB SAFE
# TF-IDF (CHAR LEVEL) + Logistic Regression
# Trains in seconds, no RAM crash.
# =============================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import re

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv("malicious_phish.csv").dropna()

label_map = {
    "benign": 0, "safe": 0,
    "malware": 1, "defacement": 1,
    "phishing": 1, "malicious": 1
}
df["type"] = df["type"].map(label_map)

# Clean
df = df.dropna().reset_index(drop=True)
print(df.head())


# -----------------------
# URL CLEANING
# -----------------------
def clean_url(x):
    x = x.lower().strip()
    x = re.sub(r'http[s]?://', '', x)
    x = re.sub(r'www\.', '', x)
    return x

df["url"] = df["url"].apply(clean_url)


# -----------------------
# TRAIN SPLIT
# -----------------------
X_train, X_test, y_train, y_test = train_test_split(
    df["url"], df["type"], test_size=0.2, random_state=42, stratify=df["type"]
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------
# TF-IDF (CHAR LEVEL) – SUPER FAST!
# -----------------------
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 6),   # character 3–6 grams
    max_features=300000,  # keeps RAM low
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec  = vectorizer.transform(X_test)


# -----------------------
# LOGISTIC REGRESSION (FAST + ACCURATE)
# -----------------------
model = LogisticRegression(
    max_iter=200,
    n_jobs=-1,
    class_weight="balanced"    # important for malicious class
)

model.fit(X_train_vec, y_train)


# -----------------------
# EVALUATION
# -----------------------
preds = model.predict(X_test_vec)

print("\nAccuracy:", accuracy_score(y_test, preds) * 100, "%")
print("\nClassification Report:\n", classification_report(
    y_test, preds, target_names=["Safe", "Malicious"]
))


# -----------------------
# SAVE MODEL
# -----------------------
import pickle
pickle.dump(model, open("url_model_lr.pkl", "wb"))
pickle.dump(vectorizer, open("tfidf_vectorizer.pkl", "wb"))

print("\nModel saved successfully!")
