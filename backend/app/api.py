# backend/app/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.utils import load_flattened_messages

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

@router.get("/messages")
def get_all_messages():
    messages = load_flattened_messages()
    return {"messages": messages}

@router.post("/search")
def search_messages(payload: SearchRequest):
    query = payload.query.lower()
    messages = load_flattened_messages()
    filtered = [msg for msg in messages if query in msg["text"].lower()]
    return {"results": filtered}
