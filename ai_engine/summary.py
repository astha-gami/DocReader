def generate_summary(info):
    doc = info.get("doc_type", "document")
    deadline = info.get("deadline")

    actions = info.get("actions_required", [])
    action_text = actions[0] if actions else None

    summary = f"This is an {doc}."

    if action_text:
        summary += f" It instructs you to {action_text.lower()}."

    if deadline:
        summary += f" The deadline is {deadline}."

    return summary



def generate_ai_advice(info):
    doc = info.get("doc_type", "")
    deadline = info.get("deadline")
    where = info.get("where_to_submit")

    if "Aadhaar" in doc:
        advice = "Visit the nearest Aadhaar Seva Kendra with original POI/POA documents."
    else:
        advice = "Submit the required documents at the mentioned office or portal."

    if deadline:
        advice += f" Complete this before {deadline}."

    if where:
        advice += f" Submission Location: {where}."

    return advice
