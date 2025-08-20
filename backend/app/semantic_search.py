# backend/app/semantic_search.py
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.utils import load_flattened_messages

# Paths for saving index + metadata
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../shared/data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "faiss_meta.json")

# Load model once (small & fast)
model = SentenceTransformer("all-MiniLM-L6-v2")

class SemanticSearchEngine:
    def __init__(self):
        self.index = None
        self.metadata = []

    def build_index(self, messages):
        """
        Build a FAISS index from message list.
        Each message is expected to have "text" + metadata (id, conversationId, etc.).
        """
        texts = [m["text"] for m in messages]
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)  # cosine similarity can be approximated with L2 norm after normalization
        index.add(embeddings)

        # Save index + metadata
        faiss.write_index(index, INDEX_PATH)
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        self.index = index
        self.metadata = messages

    def load_index(self):
        """Load FAISS index + metadata from disk."""
        if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
            raise FileNotFoundError("FAISS index or metadata not found. Run build_index first.")

        self.index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def search(self, query: str, top_k: int = 5):
        """Search top_k messages for a given query string."""
        if self.index is None or not self.metadata:
            raise RuntimeError("Index not loaded. Call load_index() at startup.")

        # Encode query
        q_vec = model.encode([query], convert_to_numpy=True)
        # Perform similarity search
        distances, indices = self.index.search(q_vec, top_k)

        results = []
        for score, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            msg = self.metadata[idx]
            results.append({
                "conversationId": msg.get("conversationId"),
                "messageId": msg.get("id"),
                "snippet": msg.get("text"),
                "participant": msg.get("participant"),
                "timestamp": msg.get("timestamp"),
                "score": float(score)
            })

        return results

# Singleton engine instance
semantic_engine = SemanticSearchEngine()

def build_and_save_index():
    """Helper for CLI / first run."""
    messages = load_flattened_messages()
    semantic_engine.build_index(messages)
    print(f"✅ FAISS index built with {len(messages)} messages.")
