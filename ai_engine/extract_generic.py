from ai_engine.extract_common import common_extract

def extract_generic(text):
    info = common_extract(text)
    info["doc_type"] = "Generic Notice or Letter"
    return info
