# backend/app/utils.py
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../shared/data/flattenedMessages.json")

def load_flattened_messages():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
