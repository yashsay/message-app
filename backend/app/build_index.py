#!/usr/bin/env python3
"""
FAISS Index Builder

This module builds a FAISS (Facebook AI Similarity Search) index from flattened message data
to enable efficient semantic search capabilities for the message application.

The script reads from `shared/data/flattenedMessages.json`, processes the messages,
and creates both a FAISS index and associated metadata mapping for fast similarity searches.

Usage:
    python -m app.build_index

Dependencies:
    - FAISS library for vector similarity search
    - Pre-processed message data in JSON format

Author: Message App Team
Version: 1.0.0
"""

import sys
import logging
from pathlib import Path

from app.semantic_search import build_and_save_index

# Configure logging for better debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main entry point for building the FAISS index.

    This function orchestrates the index building process by:
    1. Validating the environment and dependencies
    2. Building the FAISS index from message data
    3. Saving the index and metadata to disk

    Raises:
        Exception: If the index building process fails
    """
    try:
        logger.info("🔄 Starting FAISS index build process...")
        logger.info("📖 Reading data from flattenedMessages.json...")

        # Build and save the FAISS index with metadata
        build_and_save_index()

        logger.info("✅ FAISS index and metadata successfully saved to shared/data/")
        logger.info("🎉 Index build process completed successfully!")

    except FileNotFoundError as e:
        logger.error(f"❌ Required data file not found: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Failed to build FAISS index: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
