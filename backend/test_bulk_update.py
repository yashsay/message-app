"""
Test script for the bulk update API endpoint.
This script demonstrates how to use the /bulk-update endpoint.
"""

import requests
import json

# Sample conversation data (matching the format from your example)
test_conversations = [
    {
        "messageResponse": [
            {
                "messageId": "test-msg-001",
                "messageType": "OUTGOING",
                "content": "Test message for bulk update API",
                "senderName": "Test User",
                "readBy": [
                    {
                        "readUser": {
                            "type": "Patient",
                            "identifier": "TEST123",
                            "displayName": "test@example.com",
                            "firstName": "Test",
                            "lastName": "User",
                            "patientPortalId": "test-portal-id"
                        },
                        "readTimestamp": "2025-11-21T10:00:00.000Z"
                    }
                ],
                "timeStamp": "2025-11-21T10:00:00.000",
                "seen": True,
                "attachments": []
            }
        ],
        "subject": "Test Conversation",
        "purpose": "Testing",
        "participants": ["Test User", "Test Provider"],
        "status": "OPEN",
        "conversationId": "test-conversation-001"
    }
]

def test_bulk_update():
    """Test the bulk update endpoint."""

    # API endpoint (adjust port if needed)
    url = "http://localhost:8000/bulk-update"

    # Send POST request
    response = requests.post(
        url,
        json=test_conversations,
        headers={"Content-Type": "application/json"}
    )

    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("\n✅ Bulk update successful!")
    else:
        print("\n❌ Bulk update failed!")

if __name__ == "__main__":
    print("Testing bulk update endpoint...\n")
    try:
        test_bulk_update()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the FastAPI server is running on port 8000.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
