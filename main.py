from fastapi import FastAPI, Form
from pydantic import BaseModel
import pickle
import re
import requests
import os
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "url_svm_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

# -----------------------
# FastAPI setup
# -----------------------
app = FastAPI(title="Fast URL Classifier + WhatsApp Bot")

class URLInput(BaseModel):
    url: str

# -----------------------
# URL cleaning
# -----------------------
def clean_url(x):
    x = x.lower().strip()
    x = re.sub(r'http[s]?://', '', x)
    x = re.sub(r'www\.', '', x)
    return x

# -----------------------
# Prediction function
# -----------------------
def predict_url(url: str):
    url_clean = clean_url(url)
    vec = vectorizer.transform([url_clean])
    pred = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    return {
        "url": url,
        "prediction": "Malicious" if pred == 1 else "Safe",
        "safe_prob": float(proba[0]),
        "malicious_prob": float(proba[1])
    }

# -----------------------
# API route for prediction (optional)
# -----------------------
@app.post("/predict")
def predict(data: URLInput):
    return predict_url(data.url)

# -----------------------
# WhatsApp bot webhook
# -----------------------
ULTRAMSG_INSTANCE = "instance155326"
ULTRAMSG_TOKEN = "2t3u41ygtwi7dltr"
ULTRAMSG_API_URL = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE}/messages/chat"

@app.post("/whatsapp_bot")
def whatsapp_bot(
    from_number: str = Form(...),
    body: str = Form(...)
):
    """
    Receives message from WhatsApp via UltraMsg and responds with URL prediction
    """
    print("Received message from:", from_number)
    print("Message body:", body)

    url = body.strip()
    result = predict_url(url)

    reply_text = (
        f"🔍 URL Scan Result\n"
        f"URL: {result['url']}\n"
        f"Prediction: {result['prediction']}\n"
        f"Safe Probability: {result['safe_prob']:.2f}\n"
        f"Malicious Probability: {result['malicious_prob']:.2f}"
    )

    # Send reply back via UltraMsg API
    data = {
        "token": ULTRAMSG_TOKEN,
        "to": from_number,
        "body": reply_text
    }
    requests.post(ULTRAMSG_API_URL, data=data)

    return {"status": "success"}

# -----------------------
# Run server
# -----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use cloud port if available
    uvicorn.run("main:app", host="0.0.0.0", port=port)
