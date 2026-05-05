#  URL Malicious Detection System (ML + WhatsApp Bot)

##  Project Overview

This project is a **Machine Learning-based URL classification system** that detects whether a URL is **Safe or Malicious**.
It uses **character-level TF-IDF features** and a **Logistic Regression / SVM-based classifier** trained on a phishing dataset.

The system is also integrated with a **WhatsApp bot using UltraMsg API**, allowing real-time URL scanning directly from WhatsApp messages.

---

##  Key Features

* ✔ Detects **Safe vs Malicious URLs**
* ✔ Character-level **TF-IDF feature extraction**
* ✔ Fast and lightweight ML model (suitable for deployment)
* ✔ REST API using **FastAPI**
* ✔ WhatsApp bot integration using **UltraMsg**
* ✔ Real-time URL scanning via messages
* ✔ Automatic reply with prediction result
* ✔ Trained model saved using `pickle`

---

##  Machine Learning Approach

###  Dataset

* File: `malicious_phish.csv`
* Labels mapped as:

  * `benign / safe → 0`
  * `malware / phishing / defacement / malicious → 1`

###  Preprocessing

* Lowercasing URLs
* Removing `http://`, `https://`, and `www.`
* Cleaning special patterns

###  Feature Extraction

* Method: **TF-IDF Vectorization**
* Type: Character-level n-grams
* Range: `3–6 grams`
* Max features: `300,000`

###  Model

* Logistic Regression (or SVM variant used in deployment)
* Balanced class weights for handling imbalanced dataset
* Optimized for fast inference

---

##  System Architecture

```
User (WhatsApp Message)
        ↓
UltraMsg Webhook
        ↓
FastAPI Server (/whatsapp_bot)
        ↓
URL Cleaning + Feature Extraction
        ↓
ML Model Prediction
        ↓
Response sent back via WhatsApp
```

---

##  Installation & Setup

###  Clone Repository

```bash
git clone <your-repo-link>
cd url-detection-project
```

###  Install Dependencies

```bash
pip install pandas numpy scikit-learn fastapi uvicorn requests pydantic
```

###  Run Model Training (optional)

```bash
python model.py
```

This will generate:

* `url_model_lr.pkl` (trained model)
* `tfidf_vectorizer.pkl` (feature extractor)

---

##  Run FastAPI Server

```bash
uvicorn main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

---

##  WhatsApp Bot Integration

###  Setup

This project uses **UltraMsg API** for WhatsApp automation.

You must configure:

```python
ULTRAMSG_INSTANCE = "your_instance"
ULTRAMSG_TOKEN = "your_token"
```

###  Webhook Endpoint

```
POST /whatsapp_bot
```

###  Workflow

1. User sends URL on WhatsApp
2. UltraMsg forwards message to FastAPI webhook
3. Model predicts:

   * Safe 
   * Malicious 
4. Bot replies automatically on WhatsApp

---

##  Prediction Output Example

```
 URL Scan Result
URL: https://example.com
Prediction: Safe 
```

or

```
 URL Scan Result
URL: http://malicious-site.com
Prediction: Malicious 
```

---

##  Model Performance

* High-speed inference (real-time ready)
* Lightweight architecture (Colab-safe)
* Strong performance using character-level patterns

---

##  Project Structure

```
.
├── model.py                  # Model training script
├── main.py                   # FastAPI + WhatsApp bot
├── malicious_phish.csv      # Dataset
├── tfidf_vectorizer.pkl     # Saved vectorizer
├── url_model_lr.pkl         # Trained ML model
└── outputs.docx
└── flowchart.docx
```

---

##  Future Improvements

* Deep Learning model (LSTM/CNN for URLs)
* Domain reputation scoring
* Browser extension integration
* Dashboard for analytics
* Multi-class classification (phishing, malware, etc.)

---

## Author
**Hafsa Tahir (Software Engineering Student)**

Developed as a Machine Learning + Web Integration project for real-time URL threat detection.
