from ai_engine.extract_common import common_extract

def extract_gst(text):
    info = common_extract(text)
    info["doc_type"] = "GST Department Notice"
    info["recommended_action"] = "Submit GST reconciliation documents"
    return info
