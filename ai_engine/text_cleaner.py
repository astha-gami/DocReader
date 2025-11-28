import re

def clean_text(text):
    text = text.replace("\n\n", "\n")
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # remove non-ASCII
    text = re.sub(r"[ ]{2,}", " ", text)
    return text.strip()
