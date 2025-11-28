import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from ai_engine.preprocess import preprocess_image_for_ocr
import hashlib
import concurrent.futures

# ----------- TESSERACT PATH -----------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ----------- CACHE FOR OCR RESULTS -----------
ocr_cache = {}


def extract_text_from_pdf(pdf_path):
    """
    PDF → Image → Preprocess → OCR → Clean Text
    Works on scanned PDFs, blurry PDFs, government notices, forms, etc.
    """

    # ---------- Load PDF Pages ----------
    try:
        pages = convert_from_path(pdf_path, poppler_path=r"C:\poppler\bin")
    except:
        pages = convert_from_path(pdf_path)

    final_text = ""

    # ---------- Process Each Page ----------
    for i, page in enumerate(pages):
        print(f"[DEBUG] Processing page {i+1}...")

        # Convert PIL image → OpenCV BGR format
        cv_img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        # ---------- Preprocess Image ----------
        processed = preprocess_image_for_ocr(cv_img)
        # processed is clean binary image after threshold + denoise + deskew

        # ---------- OCR ----------
        text = pytesseract.image_to_string(processed)
        final_text += text + "\n\n"

    return final_text
