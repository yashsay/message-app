# backend/app/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.utils import load_flattened_messages
from app.semantic_search import semantic_engine  # ✅ import your semantic engine

router = APIRouter()

# ---------- Models ----------
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5   # default if not provided

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
