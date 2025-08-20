# backend/app/build_index.py
"""
Builds a FAISS index from shared/data/flattenedMessages.json
and saves both the FAISS index + metadata mapping.
Run this once before starting the API:
    python -m app.build_index
"""

from app.semantic_search import build_and_save_index

if __name__ == "__main__":
    print("🔄 Building FAISS index from flattenedMessages.json ...")
    build_and_save_index()
    print("✅ FAISS index and metadata saved in shared/data/")
