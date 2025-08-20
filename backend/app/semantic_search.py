
"""
semantic_search.py

Provides a semantic search engine for message data using FAISS and sentence-transformers.
This module enables building, saving, loading, and querying a vector index of messages for fast semantic search.

Key components:
- SemanticSearchEngine: Class for managing the FAISS index and metadata.
- build_and_save_index: Helper function to build and persist the index from message data.

Dependencies:
- faiss: For efficient similarity search on vector embeddings.
- sentence-transformers: For generating message embeddings.
- numpy, json, os: Standard utilities.
"""

import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.utils import load_flattened_messages

# Paths for saving index and metadata
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../shared/data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "faiss_meta.json")

# Load the sentence transformer model once (small & fast)
model = SentenceTransformer("all-MiniLM-L6-v2")

class SemanticSearchEngine:
    """
    SemanticSearchEngine manages a FAISS vector index and associated message metadata
    for efficient semantic search over a collection of messages.
    """
    def __init__(self):
        """
        Initialize the search engine with empty index and metadata.
        """
        self.index = None  # FAISS index object
        self.metadata = []  # List of message dicts

    def build_index(self, messages):
        """
        Build a FAISS index from a list of message dicts.

        Args:
            messages (list): List of dicts, each with at least a 'text' field and other metadata.

        Side effects:
            - Saves the FAISS index to INDEX_PATH
            - Saves the message metadata to META_PATH
        """
        texts = [m["text"] for m in messages]
        # Generate embeddings for all messages
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

        dim = embeddings.shape[1]
        # Use L2 index (cosine similarity can be approximated with L2 norm after normalization)
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        # Save index and metadata to disk
        faiss.write_index(index, INDEX_PATH)
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        self.index = index
        self.metadata = messages

    def load_index(self):
        """
        Load the FAISS index and message metadata from disk.

        Raises:
            FileNotFoundError: If index or metadata files are missing.
        """
        if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
            raise FileNotFoundError("FAISS index or metadata not found. Run build_index first.")

        self.index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def search(self, query: str, top_k: int = 5):
        """
        Search for the top_k most semantically similar messages to the query string.

        Args:
            query (str): The search query string.
            top_k (int): Number of top results to return.

        Returns:
            list: List of dicts with message metadata and similarity score.

        Raises:
            RuntimeError: If the index is not loaded.
        """
        if self.index is None or not self.metadata:
            raise RuntimeError("Index not loaded. Call load_index() at startup.")

        # Encode the query string to embedding
        q_vec = model.encode([query], convert_to_numpy=True)
        # Perform similarity search in the FAISS index
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

# Singleton engine instance for use throughout the app
semantic_engine = SemanticSearchEngine()

def build_and_save_index():
    """
    Helper function to build and save the FAISS index and metadata from flattened messages.
    Intended for CLI or first-run setup.
    """
    messages = load_flattened_messages()
    semantic_engine.build_index(messages)
    print(f"✅ FAISS index built with {len(messages)} messages.")
