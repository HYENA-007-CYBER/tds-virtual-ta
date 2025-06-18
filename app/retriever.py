# app/retriever.py

import json
from difflib import SequenceMatcher

def load_data():
    with open("tds_data.json", "r", encoding="utf-8") as f:
        course_data = json.load(f)
    with open("discourse_tds_kb.json", "r", encoding="utf-8") as f:
        discourse_data = json.load(f)
    return course_data, discourse_data

def find_relevant_content(question, top_k=3):
    course_data, discourse_data = load_data()

    def score(text):
        return SequenceMatcher(None, question.lower(), text["title"].lower()).ratio()

    course_scores = sorted(course_data, key=score, reverse=True)[:top_k]
    discourse_scores = sorted(discourse_data, key=score, reverse=True)[:top_k]

    return course_scores, discourse_scores
