# tools/faq_tool.py
import json, os

def load_faqs(path="data/faqs.json"):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

FAQS = load_faqs()

def find_faq_answer(query: str):
    # naive: check keywords
    q = query.lower()
    for item in FAQS:
        if any(k.lower() in q for k in item.get("keywords", [])):
            return item.get("answer")
    return None
