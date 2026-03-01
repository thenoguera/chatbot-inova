# src/feedback.py
from pathlib import Path
import json
from datetime import datetime

FEEDBACK_FILE = Path("data/feedback.jsonl")

def save_feedback(payload: dict):
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload["ts_utc"] = datetime.utcnow().isoformat() + "Z"
    with FEEDBACK_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")