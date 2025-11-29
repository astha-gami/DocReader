import re

def clean_text(text):
    if not text:
        return ""
    
    # remove tabs, extra spaces, weird characters
    text = re.sub(r"\s+", " ", text)
    text = text.replace("", " ")
    text = text.replace("\x0c", " ")  # remove page break char
    
    # remove duplicate spaces
    text = re.sub(r"\s{2,}", " ", text).strip()
    
    return text
