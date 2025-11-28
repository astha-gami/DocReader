import requests
import os

def extract_text_from_pdf_cloud(pdf_path):
    api_key = os.getenv("OCR_API_KEY")

    url = "https://api.ocr.space/parse/image"

    with open(pdf_path, 'rb') as f:
        payload = {
            'apikey': api_key,
            'language': 'eng',
            'isOverlayRequired': False
        }
        r = requests.post(url, files={'file': f}, data=payload)

    result = r.json()

    if result.get("ParsedResults"):
        return result["ParsedResults"][0]["ParsedText"]
    else:
        return ""
