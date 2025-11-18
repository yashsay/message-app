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
