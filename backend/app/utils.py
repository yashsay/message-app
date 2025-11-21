"""
Utility functions for the message app backend.

This module provides helper functions for data loading and processing operations
used throughout the backend application.
"""

import json
import os
from typing import List, Dict, Any


# Path to the flattened messages data file
DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../shared/data/flattenedMessages.json"
)

# Path to the mock messages data file
MOCK_MESSAGES_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../shared/data/mockMessages.json"
)


def load_flattened_messages() -> List[Dict[str, Any]]:
    """
    Load and return flattened messages from the JSON data file.

    This function reads the pre-processed messages data that has been
    flattened for easier consumption by the API endpoints.

    Returns:
        List[Dict[str, Any]]: A list of message dictionaries containing
                             flattened message data.

    Raises:
        FileNotFoundError: If the data file cannot be found.
        JSONDecodeError: If the file contains invalid JSON.
        IOError: If there are issues reading the file.
    """
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Messages data file not found at: {DATA_PATH}"
        )
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in messages data file: {e.msg}",
            e.doc,
            e.pos
        )
    except IOError as e:
        raise IOError(f"Error reading messages data file: {e}")


def load_mock_messages() -> List[Dict[str, Any]]:
    """
    Load and return mock messages from the JSON data file.

    This function reads the original conversation data from mockMessages.json
    which contains the full conversation structure with nested messages.

    Returns:
        List[Dict[str, Any]]: A list of conversation dictionaries.

    Raises:
        FileNotFoundError: If the data file cannot be found.
        JSONDecodeError: If the file contains invalid JSON.
        IOError: If there are issues reading the file.
    """
    try:
        with open(MOCK_MESSAGES_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        # Return empty list if file doesn't exist yet
        return []
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in mock messages data file: {e.msg}",
            e.doc,
            e.pos
        )
    except IOError as e:
        raise IOError(f"Error reading mock messages data file: {e}")


def save_mock_messages(conversations: List[Dict[str, Any]]) -> None:
    """
    Save conversations to the mockMessages.json file.

    This function writes the conversation data back to disk, overwriting
    the existing file with the updated data.

    Args:
        conversations: List of conversation dictionaries to save.

    Raises:
        IOError: If there are issues writing the file.
        TypeError: If the data cannot be serialized to JSON.
    """
    try:
        with open(MOCK_MESSAGES_PATH, "w", encoding="utf-8") as file:
            json.dump(conversations, file, indent=2, ensure_ascii=False)
    except IOError as e:
        raise IOError(f"Error writing mock messages data file: {e}")
    except TypeError as e:
        raise TypeError(f"Error serializing conversations to JSON: {e}")
