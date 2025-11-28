import joblib

model = joblib.load("models/doc_classifier.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def classify_text(text):
    X = vectorizer.transform([text])
    prediction = model.predict(X)
    return prediction[0]
