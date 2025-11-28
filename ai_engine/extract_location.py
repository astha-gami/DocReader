def extract_submission_location(text):
    keywords = ["seva kendra", "branch", "office", "portal", "centre", "center"]

    lines = text.split("\n")
    
    for line in lines:
        clean = line.strip()

        # Skip bullet lines or mixed long items
        if clean.startswith("*"):
            continue
        if len(clean) > 80:
            continue

        for k in keywords:
            if k in clean.lower():
                return clean

    return None
