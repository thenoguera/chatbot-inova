# src/metrics.py
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]
FEEDBACK_FILE = BASE_DIR / "data" / "feedback.jsonl"

def load_feedback():
    if not FEEDBACK_FILE.exists():
        return []
    rows = []
    for line in FEEDBACK_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def summarize():
    rows = load_feedback()
    total = len(rows)
    helpful = sum(1 for r in rows if r.get("helpful") is True)
    not_helpful = sum(1 for r in rows if r.get("helpful") is False)
    helpful_rate = (helpful / total) if total else 0.0

    by_intent = {}
    for r in rows:
        it = r.get("intent", "unknown")
        by_intent[it] = by_intent.get(it, 0) + 1

    return {
        "total_feedbacks": total,
        "helpful": helpful,
        "not_helpful": not_helpful,
        "helpful_rate": round(helpful_rate, 2),
        "by_intent": by_intent
    }