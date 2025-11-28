from ai_engine.extract_common import common_extract

def extract_form(text):
    info = common_extract(text)
    info["doc_type"] = "Government Form"
    info["fields_expected"] = ["Name", "Address", "Mobile", "Signature"]
    info["recommended_action"] = "Fill and submit at respective government office"
    return info
