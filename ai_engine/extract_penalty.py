import re

penalty_keywords = [
    "penalty", "fine", "suspend", "restriction", "freeze",
    "deactivated", "service disruption", "temporary suspension"
]

amount_pattern = r"(Rs\.?\s?\d+|₹\s?\d+)"

def extract_penalty(text):
    lines = text.split("\n")
    for line in lines:
        clean = line.strip()
        for k in penalty_keywords:
            if k in clean.lower():
                amounts = re.findall(amount_pattern, clean)
                return {
                    "penalty_text": clean,
                    "amount": amounts[0] if amounts else None
                }
    return None
