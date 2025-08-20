# backend/app/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from collections import Counter
from app.utils import load_flattened_messages
from app.semantic_search import semantic_engine  # ✅ import your semantic engine

router = APIRouter()

# ---------- Models ----------
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5   # default if not provided

class SummarizeRequest(BaseModel):
    conversationId: str
    scope: Optional[str] = "all"  # "all" or "last_5"

# ---------- Routes ----------
@router.get("/messages")
def get_all_messages():
    """Return all messages from flattenedMessages.json"""
    messages = load_flattened_messages()
    return {"messages": messages}

@router.post("/search")
def search_messages(payload: SearchRequest):
    """Simple keyword search"""
    query = payload.query.lower()
    messages = load_flattened_messages()
    filtered = [msg for msg in messages if query in msg["text"].lower()]
    return {"results": filtered}

@router.post("/semantic-search")
def semantic_search(payload: SearchRequest):
    """Semantic search using embeddings + FAISS"""
    results = semantic_engine.search(payload.query, payload.top_k)
    return {"query": payload.query, "results": results}

@router.post("/summarize")
def summarize_conversation(payload: SummarizeRequest):
    """Offline extractive summarization using simple word frequency"""
    messages = load_flattened_messages()
    convo_msgs = [m for m in messages if m.get("conversationId") == payload.conversationId]

    if not convo_msgs:
        return {"conversationId": payload.conversationId, "summary": "No messages found."}

    # restrict scope if requested
    if payload.scope.startswith("last_"):
        try:
            n = int(payload.scope.split("_")[1])
            convo_msgs = convo_msgs[-n:]
        except:
            pass

    texts = [m["text"] for m in convo_msgs if "text" in m]

    if not texts:
        return {"conversationId": payload.conversationId, "summary": "No text content found."}

    # word frequency
    words = " ".join(texts).lower().split()
    freq = Counter(words)

    scored = []
    for t in texts:
        score = sum(freq[w] for w in t.lower().split())
        scored.append((score, t))

    # pick top 3
    top_sentences = [s for _, s in sorted(scored, key=lambda x: x[0], reverse=True)[:3]]
    highlights = [w for w, c in freq.most_common(5) if len(w) > 3]

    return {
        "conversationId": payload.conversationId,
        "summary": " ".join(top_sentences),
        "highlights": highlights,
    }
