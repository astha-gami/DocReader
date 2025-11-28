import re

deadline_keywords = [
    "before", "by", "on or before", "last date", "due", "deadline", "no later than"
]

date_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Za-z]{3,15}\s\d{1,2},\s\d{4})"

def extract_deadline(text):
    lines = text.split("\n")
    for line in lines:
        for k in deadline_keywords:
            if k in line.lower():
                dates = re.findall(date_pattern, line)
                if dates:
                    return dates[0], line.strip()
    return None, None
