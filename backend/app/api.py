"""
Message App API Routes

This module defines the FastAPI routes for the message application, providing
endpoints for message retrieval, search functionality, and conversation summarization.

Author: Message App Team
Date: November 2024
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from collections import Counter
import logging
import json
import os
import subprocess
import sys

from app.utils import load_flattened_messages, load_mock_messages, save_mock_messages
from app.semantic_search import semantic_engine

# Configure logging
logger = logging.getLogger(__name__)

# Initialize API router
router = APIRouter()


# ==================== REQUEST/RESPONSE MODELS ====================

class SearchRequest(BaseModel):
    """
    Request model for search operations.

    Attributes:
        query: The search query string
        top_k: Maximum number of results to return (default: 5)
    """
    query: str = Field(..., description="Search query string", min_length=1)
    top_k: int = Field(default=5, description="Maximum number of results", ge=1, le=50)


class SummarizeRequest(BaseModel):
    """
    Request model for conversation summarization.

    Attributes:
        conversationId: Unique identifier for the conversation
        scope: Scope of summarization - "all" for entire conversation or "last_N" for recent messages
    """
    conversationId: str = Field(..., description="Conversation identifier", min_length=1)
    scope: Optional[str] = Field(
        default="all",
        description="Summarization scope: 'all' or 'last_N' where N is number of messages"
    )


class User(BaseModel):
    """User information model."""
    type: str
    identifier: str
    displayName: str
    firstName: str
    lastName: str
    patientPortalId: Optional[str] = None


class ReadBy(BaseModel):
    """Read status model."""
    readUser: User
    readTimestamp: str


class Attachment(BaseModel):
    """Message attachment model."""
    createdBy: User
    updatedBy: User
    createdDate: str
    updatedDate: str
    name: str
    mimeType: str
    bytes: int
    storagePath: str


class Message(BaseModel):
    """Individual message model."""
    messageId: str
    messageType: str
    content: str
    senderName: str
    readBy: List[ReadBy]
    timeStamp: str
    seen: bool
    attachments: Optional[List[Attachment]] = None


class Conversation(BaseModel):
    """Conversation model containing messages and metadata."""
    conversationId: str
    subject: str
    purpose: str
    participants: List[str]
    status: str
    messageResponse: List[Message]


class MessageResponse(BaseModel):
    """Standard response model for message operations."""
    messages: List[Dict[str, Any]]


class SearchResponse(BaseModel):
    """Response model for search operations."""
    query: Optional[str] = None
    results: List[Dict[str, Any]]


class SummaryResponse(BaseModel):
    """Response model for summarization operations."""
    conversationId: str
    summary: str
    highlights: Optional[List[str]] = None


class BulkUpdateResponse(BaseModel):
    """Response model for bulk conversation updates."""
    success: bool
    message: str
    conversationsProcessed: int
    conversationsAdded: int
    conversationsUpdated: int
    messagesAdded: int


# ==================== API ENDPOINTS ====================

@router.get("/messages", response_model=MessageResponse)
async def get_all_messages() -> Dict[str, Any]:
    """
    Retrieve all messages from the flattened messages dataset.

    Returns:
        Dictionary containing all messages from flattenedMessages.json

    Raises:
        HTTPException: If messages cannot be loaded
    """
    try:
        logger.info("Fetching all messages")
        messages = load_flattened_messages()
        logger.info(f"Successfully loaded {len(messages)} messages")
        return {"messages": messages}
    except Exception as e:
        logger.error(f"Error loading messages: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load messages")


@router.post("/search", response_model=SearchResponse)
async def search_messages(payload: SearchRequest) -> Dict[str, Any]:
    """
    Perform keyword-based search through messages.

    This endpoint performs case-insensitive substring matching against
    message text content.

    Args:
        payload: SearchRequest containing query and top_k parameters

    Returns:
        Dictionary containing search results

    Raises:
        HTTPException: If search operation fails
    """
    try:
        logger.info(f"Performing keyword search for query: '{payload.query}'")

        query_lower = payload.query.lower()
        messages = load_flattened_messages()

        # Filter messages containing the query string
        filtered_messages = [
            msg for msg in messages
            if query_lower in msg.get("text", "").lower()
        ]

        # Limit results to top_k
        results = filtered_messages[:payload.top_k]

        logger.info(f"Keyword search returned {len(results)} results")
        return {"results": results}

    except Exception as e:
        logger.error(f"Error in keyword search: {str(e)}")
        raise HTTPException(status_code=500, detail="Search operation failed")


@router.post("/semantic-search", response_model=SearchResponse)
async def semantic_search(payload: SearchRequest) -> Dict[str, Any]:
    """
    Perform semantic search using vector embeddings and FAISS indexing.

    This endpoint uses pre-computed embeddings and FAISS for efficient
    similarity-based message retrieval.

    Args:
        payload: SearchRequest containing query and top_k parameters

    Returns:
        Dictionary containing semantic search results with similarity scores

    Raises:
        HTTPException: If semantic search engine is unavailable or search fails
    """
    try:
        logger.info(f"Performing semantic search for query: '{payload.query}'")

        # Perform semantic search using the engine
        results = semantic_engine.search(payload.query, payload.top_k)

        logger.info(f"Semantic search returned {len(results)} results")
        return {
            "query": payload.query,
            "results": results
        }

    except Exception as e:
        logger.error(f"Error in semantic search: {str(e)}")
        raise HTTPException(status_code=500, detail="Semantic search operation failed")


@router.post("/summarize", response_model=SummaryResponse)
async def summarize_conversation(payload: SummarizeRequest) -> Dict[str, Any]:
    """
    Generate an extractive summary of a conversation using word frequency analysis.

    This endpoint creates summaries by:
    1. Filtering messages by conversation ID
    2. Optionally limiting to recent messages based on scope
    3. Computing word frequency scores
    4. Selecting top-scoring sentences for the summary
    5. Identifying key highlight terms

    Args:
        payload: SummarizeRequest containing conversationId and scope

    Returns:
        Dictionary containing conversation summary and highlights

    Raises:
        HTTPException: If conversation not found or summarization fails
    """
    try:
        logger.info(f"Summarizing conversation: {payload.conversationId}")

        # Load all messages and filter by conversation ID
        messages = load_flattened_messages()
        conversation_messages = [
            msg for msg in messages
            if msg.get("conversationId") == payload.conversationId
        ]

        if not conversation_messages:
            logger.warning(f"No messages found for conversation: {payload.conversationId}")
            return {
                "conversationId": payload.conversationId,
                "summary": "No messages found for this conversation.",
                "highlights": []
            }

        # Apply scope restriction if specified
        if payload.scope and payload.scope.startswith("last_"):
            try:
                # Extract number from "last_N" format
                num_messages = int(payload.scope.split("_")[1])
                conversation_messages = conversation_messages[-num_messages:]
                logger.info(f"Limited scope to last {num_messages} messages")
            except (IndexError, ValueError) as e:
                logger.warning(f"Invalid scope format '{payload.scope}': {e}. Using all messages.")

        # Extract text content from messages
        message_texts = [
            msg["text"] for msg in conversation_messages
            if msg.get("text")
        ]

        if not message_texts:
            return {
                "conversationId": payload.conversationId,
                "summary": "No text content found in this conversation.",
                "highlights": []
            }

        # Compute word frequency for scoring
        all_words = " ".join(message_texts).lower().split()
        word_frequency = Counter(all_words)

        # Score each message based on word frequency
        scored_messages = []
        for text in message_texts:
            # Calculate cumulative frequency score for the message
            words_in_text = text.lower().split()
            score = sum(word_frequency[word] for word in words_in_text)
            scored_messages.append((score, text))

        # Select top 3 highest-scoring sentences for summary
        top_sentences = [
            sentence for _, sentence in
            sorted(scored_messages, key=lambda x: x[0], reverse=True)[:3]
        ]

        # Generate highlight terms (most common words with length > 3)
        highlight_words = [
            word for word, count in word_frequency.most_common(5)
            if len(word) > 3
        ]

        summary = " ".join(top_sentences)
        logger.info(f"Generated summary with {len(top_sentences)} sentences")

        return {
            "conversationId": payload.conversationId,
            "summary": summary,
            "highlights": highlight_words
        }

    except Exception as e:
        logger.error(f"Error summarizing conversation {payload.conversationId}: {str(e)}")
        raise HTTPException(status_code=500, detail="Conversation summarization failed")


@router.post("/bulk-update", response_model=BulkUpdateResponse)
async def bulk_update_conversations(conversations: List[Conversation]) -> Dict[str, Any]:
    """
    Bulk update conversations by adding new conversations or merging messages into existing ones.

    This endpoint:
    1. Loads existing conversations from mockMessages.json
    2. For each conversation in the request:
       - If conversationId doesn't exist, adds the full conversation
       - If conversationId exists, merges new messages (avoiding duplicates)
    3. Saves the updated mockMessages.json
    4. Calls flattenMessages() to regenerate flattenedMessages.json
    5. Calls buildIndex() to rebuild the FAISS search index

    Args:
        conversations: List of Conversation objects to add or update

    Returns:
        Dictionary containing operation statistics and success status

    Raises:
        HTTPException: If the operation fails
    """
    try:
        logger.info(f"Starting bulk update with {len(conversations)} conversations")

        # Load existing conversations from mockMessages.json
        existing_conversations = load_mock_messages()
        logger.info(f"Loaded {len(existing_conversations)} existing conversations")

        # Track statistics
        conversations_added = 0
        conversations_updated = 0
        messages_added = 0

        # Process each conversation in the request
        for new_conversation in conversations:
            # Find if conversation already exists
            existing_index = None
            for idx, conv in enumerate(existing_conversations):
                if conv.get("conversationId") == new_conversation.conversationId:
                    existing_index = idx
                    break

            if existing_index is None:
                # Conversation doesn't exist - add it completely
                existing_conversations.append(new_conversation.dict())
                conversations_added += 1
                messages_added += len(new_conversation.messageResponse)
                logger.info(f"Added new conversation: {new_conversation.conversationId}")
            else:
                # Conversation exists - merge messages
                existing_conv = existing_conversations[existing_index]
                existing_message_ids = {
                    msg.get("messageId")
                    for msg in existing_conv.get("messageResponse", [])
                }

                # Add only new messages (not already present)
                new_messages_count = 0
                for new_message in new_conversation.messageResponse:
                    if new_message.messageId not in existing_message_ids:
                        existing_conv["messageResponse"].append(new_message.dict())
                        new_messages_count += 1
                        messages_added += 1

                if new_messages_count > 0:
                    conversations_updated += 1
                    logger.info(
                        f"Updated conversation {new_conversation.conversationId}: "
                        f"added {new_messages_count} new messages"
                    )

                # Update conversation metadata
                existing_conv["subject"] = new_conversation.subject
                existing_conv["purpose"] = new_conversation.purpose
                existing_conv["participants"] = new_conversation.participants
                existing_conv["status"] = new_conversation.status

        # Save updated conversations to mockMessages.json
        save_mock_messages(existing_conversations)
        logger.info("Successfully saved updated mockMessages.json")

        # Call flattenMessages script
        logger.info("Running flattenMessages.py...")
        flatten_script_path = os.path.join(
            os.path.dirname(__file__),
            "../../shared/scripts/flattenMessages.py"
        )
        subprocess.run(
            [sys.executable, flatten_script_path],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Successfully flattened messages")

        # Call buildIndex
        logger.info("Rebuilding FAISS index...")
        from app.semantic_search import build_and_save_index
        build_and_save_index()
        logger.info("Successfully rebuilt FAISS index")

        return {
            "success": True,
            "message": "Conversations updated successfully",
            "conversationsProcessed": len(conversations),
            "conversationsAdded": conversations_added,
            "conversationsUpdated": conversations_updated,
            "messagesAdded": messages_added
        }

    except subprocess.CalledProcessError as e:
        logger.error(f"Error running post-processing scripts: {str(e)}")
        logger.error(f"Script output: {e.stderr}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run post-processing: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error in bulk update: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Bulk update operation failed: {str(e)}"
        )
