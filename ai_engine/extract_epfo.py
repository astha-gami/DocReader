from ai_engine.extract_common import common_extract

def extract_epfo(text):
    info = common_extract(text)
    info["doc_type"] = "EPFO / PF Notice"
    info["recommended_action"] = "Update KYC on EPFO portal or visit PF office"
    return info
