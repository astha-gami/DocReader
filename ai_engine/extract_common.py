import re
import spacy

nlp = spacy.blank("en")


# --------- DATE ---------
date_pattern = r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b"

def extract_dates(text):
    return re.findall(date_pattern, text)

# --------- NOTICE NO ---------
notice_pattern = r"(Ref\s?No[:\s]*[A-Za-z0-9\/-]+)"

def extract_notice_number(text):
    return re.findall(notice_pattern, text)

# --------- AMOUNTS ---------
amount_pattern = r"(Rs\.?\s?\d+|₹\s?\d+|INR\s?\d+)"

def extract_amounts(text):
    return re.findall(amount_pattern, text)

# --------- ACTION LINES ---------
action_keywords = [
    "submit", "update", "required", "must", "visit",
    "provide", "carry"
]

def extract_actions(text):
    lines = text.split("\n")
    actions = []

    for line in lines:
        clean = line.strip()

        # Skip very long lines (avoid full paragraphs)
        if len(clean) > 120:
            continue

        # Skip short useless lines
        if len(clean) < 10:
            continue

        # Check for action keywords
        if any(k in clean.lower() for k in action_keywords):
            actions.append(clean)

    # Limit to top 3 meaningful lines
    return sorted(actions, key=len)[:3]   # smallest, most meaningful lines first



# --------- ENTITIES ---------
def extract_entities(text):
    doc = nlp(text)
    entities = {"PERSON": [], "ORG": [], "GPE": []}

    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)

    return entities

# --------- FINAL COMBINED ---------
def common_extract(text):
    return {
        "dates": extract_dates(text),
        "notice_numbers": extract_notice_number(text),
        "amounts": extract_amounts(text),
        "actions_required": extract_actions(text),
        "entities": extract_entities(text)
    }
