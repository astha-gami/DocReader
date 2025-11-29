import joblib

model = joblib.load("models/doc_classifier.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def classify_text(text):
    if not text:
        return "generic_notice"

    text = text.lower()

    # basic keyword fallback (fixes cloud OCR failures)
    if "aadhaar" in text or "uidai" in text:
        return "aadhaar_notice"
    if "kyc" in text or "bank" in text:
        return "bank_kyc_notice"
    if "epfo" in text or "pf" in text:
        return "epfo_notice"
    if "gst" in text:
        return "gst_notice"

    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    return pred
