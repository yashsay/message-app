
"""
Semantic Search Engine for Message Data

This module provides a comprehensive semantic search solution for message data using
FAISS (Facebook AI Similarity Search) and sentence-transformers for generating
high-quality embeddings.

The module enables efficient building, persistence, loading, and querying of vector
indices for fast semantic similarity search across large message datasets.

Classes:
    SemanticSearchEngine: Core class for managing FAISS index and associated metadata

Functions:
    build_and_save_index: Utility function to build and persist the search index

Technical Dependencies:
    - faiss-cpu: High-performance similarity search and clustering library
    - sentence-transformers: State-of-the-art sentence embeddings
    - numpy: Numerical computing support
    - json: Data serialization
    - os: File system operations

Author: Message App Team
Version: 1.0.0
"""

import os
import json
from typing import List, Dict, Any, Optional

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.utils import load_flattened_messages


# Configuration constants
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../shared/data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
META_PATH = os.path.join(DATA_DIR, "faiss_meta.json")

# Model configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Lightweight, fast model with good performance

# Initialize the sentence transformer model globally for efficiency
# This model provides 384-dimensional embeddings with good semantic understanding
model = SentenceTransformer(EMBEDDING_MODEL)

class SemanticSearchEngine:
    """
    A high-performance semantic search engine for message data.

    This class manages a FAISS vector index and associated message metadata to enable
    efficient semantic similarity search across large collections of messages. It uses
    pre-trained transformer models to generate embeddings and FAISS for fast retrieval.

    Attributes:
        index (faiss.Index): The FAISS vector index for similarity search
        metadata (List[Dict[str, Any]]): Message metadata corresponding to index entries

    Example:
        >>> engine = SemanticSearchEngine()
        >>> engine.load_index()
        >>> results = engine.search("hello world", top_k=5)
    """

    def __init__(self) -> None:
        """
        Initialize the semantic search engine.

        Creates an empty search engine instance. Call load_index() to load
        a previously built index, or build_index() to create a new one.
        """
        self.index: Optional[faiss.Index] = None
        self.metadata: List[Dict[str, Any]] = []

    def build_index(self, messages: List[Dict[str, Any]]) -> None:
        """
        Build a FAISS vector index from message data.

        Creates embeddings for all message text content and constructs a FAISS index
        for efficient similarity search. Automatically saves the index and metadata
        to disk for persistence.

        Args:
            messages: List of message dictionaries. Each message must contain
                     a 'text' field and may include additional metadata fields
                     such as 'id', 'conversationId', 'participant', 'timestamp'.

        Raises:
            KeyError: If messages are missing required 'text' field
            OSError: If unable to write index or metadata files

        Side Effects:
            - Saves FAISS index to disk at INDEX_PATH
            - Saves message metadata to disk at META_PATH
            - Updates instance attributes (index, metadata)

        Note:
            This operation may take significant time for large message collections
            as it involves generating embeddings for all text content.
        """
        if not messages:
            raise ValueError("Cannot build index from empty message list")

        # Extract text content for embedding generation
        texts = [message["text"] for message in messages]

        # Generate high-quality embeddings using pre-trained transformer model
        # show_progress_bar provides user feedback for long operations
        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
            batch_size=32  # Optimize memory usage for large datasets
        )

        # Create FAISS index with Inner Product for true cosine similarity
        # Inner Product on normalized embeddings gives exact cosine similarity
        # This provides more accurate semantic similarity measurements
        embedding_dimension = embeddings.shape[1]

        # Ensure embeddings are properly normalized for cosine similarity
        faiss.normalize_L2(embeddings)

        # Use Inner Product index for cosine similarity
        index = faiss.IndexFlatIP(embedding_dimension)

        # Add all embeddings to the index in a single operation
        index.add(embeddings.astype(np.float32))

        # Ensure data directory exists before saving
        os.makedirs(DATA_DIR, exist_ok=True)

        # Persist index and metadata to disk for future use
        faiss.write_index(index, INDEX_PATH)
        with open(META_PATH, "w", encoding="utf-8") as metadata_file:
            json.dump(messages, metadata_file, ensure_ascii=False, indent=2)

        # Update instance state
        self.index = index
        self.metadata = messages

    def load_index(self) -> None:
        """
        Load a previously built FAISS index and metadata from persistent storage.

        This method loads both the vector index and associated message metadata
        that were previously saved using build_index().

        Raises:
            FileNotFoundError: If either the FAISS index file or metadata file
                              cannot be found at their expected locations.
            json.JSONDecodeError: If the metadata file contains invalid JSON.
            RuntimeError: If the FAISS index file is corrupted or incompatible.

        Note:
            This method should be called once during application startup to
            initialize the search engine with previously built indices.
        """
        # Validate that both required files exist
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(
                f"FAISS index file not found at {INDEX_PATH}. "
                "Please run build_index() first to create the search index."
            )

        if not os.path.exists(META_PATH):
            raise FileNotFoundError(
                f"Metadata file not found at {META_PATH}. "
                "Please run build_index() first to create the metadata."
            )

        try:
            # Load the FAISS vector index from disk
            self.index = faiss.read_index(INDEX_PATH)

            # Load the corresponding message metadata
            with open(META_PATH, "r", encoding="utf-8") as metadata_file:
                self.metadata = json.load(metadata_file)

        except Exception as error:
            # Reset state on any loading error
            self.index = None
            self.metadata = []
            raise RuntimeError(f"Failed to load search index: {error}") from error

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic similarity search against the message index.

        Finds the most semantically similar messages to the given query string
        using vector similarity search in the embedded space.

        Args:
            query: The search query string. Can be a question, keywords, or
                  any natural language text to search for.
            top_k: Maximum number of results to return. Must be positive.
                  Defaults to 5.

        Returns:
            A list of dictionaries containing search results, ordered by
            similarity score (higher scores indicate higher similarity).
            Each result contains:
            - conversationId: ID of the conversation containing the message
            - messageId: Unique identifier of the message
            - snippet: The actual message text content
            - participant: Message author/sender information (alias for sender)
            - sender: Message author/sender information
            - timestamp: When the message was sent
            - score: Cosine similarity score (higher = more similar, range 0-1)

        Raises:
            RuntimeError: If the search index has not been loaded
            ValueError: If top_k is not a positive integer

        Example:
            >>> results = engine.search("project deadline", top_k=3)
            >>> for result in results:
            ...     print(f"Similarity: {result['score']:.3f} - {result['snippet'][:50]}...")
        """
        # Validate search engine state
        if self.index is None or not self.metadata:
            raise RuntimeError(
                "Search index not initialized. Call load_index() before searching."
            )

        # Validate parameters
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string")

        if not isinstance(top_k, int) or top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        # Ensure we don't request more results than available
        max_results = min(top_k, len(self.metadata))

        # Generate embedding for the search query
        # Note: We pass a list to encode() as it expects batch input
        query_embedding = model.encode([query], convert_to_numpy=True)

        # Normalize query embedding for cosine similarity
        faiss.normalize_L2(query_embedding)

        # Perform vector similarity search using FAISS
        # Returns similarity scores (higher = more similar) and indices of closest vectors
        similarity_scores, indices = self.index.search(query_embedding, max_results)

        # Transform raw results into structured response format
        search_results = []
        for similarity_score, message_index in zip(similarity_scores[0], indices[0]):
            # Skip invalid indices (FAISS returns -1 for padding in some cases)
            if message_index == -1 or message_index >= len(self.metadata):
                continue

            message_data = self.metadata[message_index]

            # Structure the result with all relevant message information
            # Note: With cosine similarity, higher scores indicate better matches
            search_result = {
                "conversationId": message_data.get("conversationId"),
                "messageId": message_data.get("messageId"),
                "snippet": message_data.get("text"),
                "participant": message_data.get("sender"),
                "sender": message_data.get("sender"),
                "timestamp": message_data.get("timestamp"),
                "score": float(similarity_score)  # Cosine similarity score (higher = more similar)
            }

            search_results.append(search_result)

        return search_results

# Global search engine instance for application-wide use
# This singleton pattern ensures consistent index state across the application
semantic_engine = SemanticSearchEngine()


def build_and_save_index() -> None:
    """
    Build and persist a new search index from current message data.

    This utility function loads all flattened message data and creates a new
    FAISS index with corresponding metadata. It's intended for initial setup,
    data refresh, or CLI operations.

    The function uses the global semantic_engine instance and automatically
    saves the results to persistent storage.

    Raises:
        FileNotFoundError: If the source message data file cannot be found
        ValueError: If the loaded message data is empty or invalid
        OSError: If unable to write the index or metadata files

    Example:
        This function is typically called during application setup or
        when message data has been updated:

        >>> build_and_save_index()
        ✅ FAISS index built with 1,234 messages.

    Note:
        This operation can be time-intensive for large message collections
        as it processes all text content through the embedding model.
    """
    try:
        # Load the complete message dataset
        messages = load_flattened_messages()

        if not messages:
            raise ValueError("No messages found to build index from")

        # Build the search index using the global engine instance
        semantic_engine.build_index(messages)

        # Provide user feedback on successful completion
        print(f"✅ FAISS index successfully built with {len(messages):,} messages.")

    except Exception as error:
        print(f"❌ Failed to build search index: {error}")
        raise
