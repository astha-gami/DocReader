def generate_summary(info):
    doc_type = info.get("doc_type", "document")
    deadline = info.get("deadline", "Not found")

    return f"This is a {doc_type}. Deadline: {deadline}. Required documents: {', '.join(info.get('requires_documents', []))}."




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
