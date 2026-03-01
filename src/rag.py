# src/rag.py
from pathlib import Path
import re
from typing import List, Tuple

KB_DIR = Path("docs/knowledge")

def _tokenize(text: str) -> List[str]:
    text = text.lower()
    return re.findall(r"[a-zà-ú0-9]+", text)

def _score(query_tokens: set, doc_tokens: List[str]) -> float:
    if not doc_tokens:
        return 0.0
    doc_set = set(doc_tokens)
    inter = len(query_tokens & doc_set)
    return inter / (len(query_tokens) + 1e-9)

def retrieve(query: str, top_k: int = 1) -> List[Tuple[str, str, float]]:
    """
    Retorna lista de (filename, snippet, score)
    """
    query_tokens = set(_tokenize(query))
    results = []

    if not KB_DIR.exists():
        return []

    for fp in KB_DIR.glob("*.*"):
        content = fp.read_text(encoding="utf-8", errors="ignore")
        tokens = _tokenize(content)
        s = _score(query_tokens, tokens)

        # snippet: primeiras ~400 chars
        snippet = content.strip().replace("\n", " ")
        snippet = snippet[:400] + ("..." if len(snippet) > 400 else "")

        results.append((fp.name, snippet, s))

    results.sort(key=lambda x: x[2], reverse=True)
    return results[:top_k]