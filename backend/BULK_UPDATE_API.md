# Bulk Update API Documentation

## Overview

The `/bulk-update` POST endpoint allows you to add new conversations or update existing conversations in the message app. It automatically handles deduplication, flattens messages, and rebuilds the search index.

## Endpoint

```
POST /bulk-update
```

## Request Body

The endpoint accepts an array of conversation objects with the following structure:

```json
[
  {
    "conversationId": "unique-conversation-id",
    "subject": "Conversation subject",
    "purpose": "Purpose of conversation",
    "participants": ["Participant 1", "Participant 2"],
    "status": "OPEN|CLOSED",
    "messageResponse": [
      {
        "messageId": "unique-message-id",
        "messageType": "OUTGOING|INCOMING|START_AUTOMATED|CLOSE_AUTOMATED",
        "content": "Message content",
        "senderName": "Sender Name",
        "timeStamp": "2025-11-21T10:00:00.000",
        "seen": true,
        "readBy": [
          {
            "readUser": {
              "type": "Patient|Provider",
              "identifier": "user-identifier",
              "displayName": "display name",
              "firstName": "First",
              "lastName": "Last",
              "patientPortalId": "optional-portal-id"
            },
            "readTimestamp": "2025-11-21T10:00:00.000Z"
          }
        ],
        "attachments": [
          {
            "createdBy": {
              /* User object */
            },
            "updatedBy": {
              /* User object */
            },
            "createdDate": "2025-11-21T10:00:00.000Z",
            "updatedDate": "2025-11-21T10:00:00.000Z",
            "name": "filename.ext",
            "mimeType": "image/jpg",
            "bytes": 1024,
            "storagePath": "path/to/file"
          }
        ]
      }
    ]
  }
]
```

## Response

Success response (200 OK):

```json
{
  "success": true,
  "message": "Conversations updated successfully",
  "conversationsProcessed": 2,
  "conversationsAdded": 1,
  "conversationsUpdated": 1,
  "messagesAdded": 5
}
```

Error response (500):

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Behavior

### Adding New Conversations

If a `conversationId` is not found in the existing `mockMessages.json`:

- The entire conversation object is added
- All messages in the conversation are included
- Statistics are updated with `conversationsAdded` count

### Updating Existing Conversations

If a `conversationId` already exists:

1. The endpoint compares messages by `messageId`
2. Only messages with new `messageId` values are appended
3. Duplicate messages (same `messageId`) are skipped
4. Conversation metadata (subject, purpose, participants, status) is updated
5. Statistics are updated with `conversationsUpdated` and `messagesAdded` counts

### Post-Processing

After updating `mockMessages.json`, the endpoint automatically:

1. Calls `flattenMessages.py` to regenerate `flattenedMessages.json`
2. Calls `buildIndex()` to rebuild the FAISS search index
3. Returns a success response with operation statistics

## Example Usage

### Python (using requests)

```python
import requests

conversations = [
    {
        "conversationId": "conv-001",
        "subject": "Medication Refills",
        "purpose": "Medication Request",
        "participants": ["Dr. Smith", "John Doe"],
        "status": "OPEN",
        "messageResponse": [
            {
                "messageId": "msg-001",
                "messageType": "OUTGOING",
                "content": "I need a refill on my prescription",
                "senderName": "John Doe",
                "timeStamp": "2025-11-21T10:00:00.000",
                "seen": True,
                "readBy": [],
                "attachments": []
            }
        ]
    }
]

response = requests.post(
    "http://localhost:8000/bulk-update",
    json=conversations
)

print(response.json())
```

### cURL

```bash
curl -X POST http://localhost:8000/bulk-update \
  -H "Content-Type: application/json" \
  -d '[
    {
      "conversationId": "conv-001",
      "subject": "Test Subject",
      "purpose": "Testing",
      "participants": ["User 1"],
      "status": "OPEN",
      "messageResponse": [
        {
          "messageId": "msg-001",
          "messageType": "OUTGOING",
          "content": "Test message",
          "senderName": "Test User",
          "timeStamp": "2025-11-21T10:00:00.000",
          "seen": true,
          "readBy": [],
          "attachments": []
        }
      ]
    }
  ]'
```

### JavaScript (using fetch)

```javascript
const conversations = [
  {
    conversationId: "conv-001",
    subject: "Test Subject",
    purpose: "Testing",
    participants: ["User 1"],
    status: "OPEN",
    messageResponse: [
      {
        messageId: "msg-001",
        messageType: "OUTGOING",
        content: "Test message",
        senderName: "Test User",
        timeStamp: "2025-11-21T10:00:00.000",
        seen: true,
        readBy: [],
        attachments: [],
      },
    ],
  },
];

fetch("http://localhost:8000/bulk-update", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(conversations),
})
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error("Error:", error));
```

## Error Handling

The endpoint may return errors in the following cases:

- **400 Bad Request**: Invalid request body format or missing required fields
- **500 Internal Server Error**:
  - Failed to read/write `mockMessages.json`
  - Error running `flattenMessages.py` script
  - Error building FAISS index
  - General processing errors

Check the error `detail` field for specific information about what went wrong.

## Testing

To test the endpoint:

1. Start the FastAPI server:

   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Run the test script:

   ```bash
   python test_bulk_update.py
   ```

3. Or use the provided example data in your request

## Notes

- The endpoint is idempotent for message additions (duplicate messageIds are skipped)
- Conversation metadata is always updated with the latest values
- The FAISS index rebuild may take a few seconds depending on the dataset size
- All timestamps should be in ISO 8601 format
