from ai_engine.ocr_cloud import extract_text_from_pdf_cloud
from ai_engine.classifier import classify_text

from ai_engine.extract_aadhaar import extract_aadhaar
from ai_engine.extract_kyc import extract_kyc
from ai_engine.extract_form import extract_form
from ai_engine.extract_generic import extract_generic
from ai_engine.extract_epfo import extract_epfo
from ai_engine.extract_gst import extract_gst

from ai_engine.text_cleaner import clean_text
from ai_engine.extract_deadline import extract_deadline
from ai_engine.extract_penalty import extract_penalty
from ai_engine.extract_location import extract_submission_location
from ai_engine.summary import generate_summary, generate_ai_advice

import hashlib

# Global cache for OCR results
ocr_cache = {}


def analyze_document(pdf_path):

    raw_text = extract_text_from_pdf_cloud(pdf_path)

    text = clean_text(raw_text)

    doc_type = classify_text(text).lower()
    print("Predicted:", doc_type)

    # BASIC EXTRACTION
    if "aadhaar" in doc_type:
        info = extract_aadhaar(text)
    elif "kyc" in doc_type or "bank" in doc_type:
        info = extract_kyc(text)
    elif "form" in doc_type:
        info = extract_form(text)
    elif "epfo" in doc_type or "pf" in doc_type:
        info = extract_epfo(text)
    elif "gst" in doc_type:
        info = extract_gst(text)
    else:
        info = extract_generic(text)

    # ADVANCED EXTRACTION
    deadline, sentence = extract_deadline(text)
    info["deadline"] = deadline
    info["deadline_sentence"] = sentence

    info["penalty"] = extract_penalty(text)
    info["where_to_submit"] = extract_submission_location(text)

    # FINAL AI OUTPUTS
    info["summary"] = generate_summary(info)
    info["ai_advice"] = generate_ai_advice(info)

# handle missing fields
    info["dates"] = info.get("dates", []) or ["Not found"]
    info["notice_numbers"] = info.get("notice_numbers", []) or ["Not found"]
    info["actions_required"] = info.get("actions_required", []) or ["Not found"]
    info["recommended_action"] = info.get("recommended_action", "Not found")
    info["deadline"] = info.get("deadline", "Not found")
    info["where_to_submit"] = info.get("where_to_submit", "Not found")

    info["raw_text"] = text

    return info
