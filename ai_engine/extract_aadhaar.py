from ai_engine.extract_common import common_extract

def extract_aadhaar(text):
    info = common_extract(text)
    info["doc_type"] = "Aadhaar Update Notice"
    info["requires_documents"] = [
        "Proof of Identity",
        "Proof of Address",
        "Recent Photograph"
    ]
    info["recommended_action"] = "Visit Aadhaar Seva Kendra or update online"
    return info
