from ai_engine.extract_common import common_extract

def extract_kyc(text):
    info = common_extract(text)
    info["doc_type"] = "Bank KYC Notice"
    info["required_documents"] = ["PAN", "Aadhaar", "Address Proof", "Photo"]
    info["recommended_action"] = "Submit documents at nearest bank branch"
    return info
