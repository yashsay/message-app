"""
Example data for testing the bulk update API endpoint.
This matches the exact format from the user's requirements.
"""

EXAMPLE_CONVERSATIONS = [
    {
        "messageResponse": [
            {
                "messageId": "151ef292-5ff9-4f4a-92d0-f9b2bde79afe",
                "messageType": "OUTGOING",
                "content": "Message for Medication Refills",
                "senderName": "Ajayy",
                "readBy": [
                    {
                        "readUser": {
                            "type": "Patient",
                            "identifier": "F8C4AF9A56204EB681AF1F7BF9D386CF",
                            "displayName": "watson_james@yopmail.com",
                            "firstName": "Ajayy",
                            "lastName": "kase Brewerr",
                            "patientPortalId": "13040a60-e403-45ae-8a99-5b6cb0c40daa"
                        },
                        "readTimestamp": "2025-01-07T05:35:04.148Z"
                    }
                ],
                "timeStamp": "2025-01-07T11:05:04.148",
                "seen": True,
                "attachments": [
                    {
                        "createdBy": {
                            "type": "Patient",
                            "identifier": "F8C4AF9A56204EB681AF1F7BF9D386CF",
                            "displayName": "watson_james@yopmail.com",
                            "firstName": "Ajayy",
                            "lastName": "kase Brewerr",
                            "patientPortalId": "13040a60-e403-45ae-8a99-5b6cb0c40daa"
                        },
                        "updatedBy": {
                            "type": "Provider",
                            "identifier": "F15FA839D7C642FBB9DA4FB586074CC5",
                            "displayName": "Ontada Test",
                            "firstName": "Ontada",
                            "lastName": "Test"
                        },
                        "createdDate": "2025-01-07T05:35:04.148Z",
                        "updatedDate": "2025-01-07T05:35:09.036Z",
                        "name": "mcp.log",
                        "mimeType": "image/jpg",
                        "bytes": 2024,
                        "storagePath": "mcp/mcp.log"
                    }
                ]
            },
            {
                "messageId": "0a7e8f7c-ce20-4816-b97b-4ec75cd04534",
                "messageType": "START_AUTOMATED",
                "content": "We have successfully received your message. Your care team will contact you shortly.",
                "senderName": "Automated message",
                "readBy": [
                    {
                        "readUser": {
                            "type": "Patient",
                            "identifier": "F8C4AF9A56204EB681AF1F7BF9D386CF",
                            "displayName": "watson_james@yopmail.com",
                            "firstName": "Ajayy",
                            "lastName": "kase Brewerr",
                            "patientPortalId": "13040a60-e403-45ae-8a99-5b6cb0c40daa"
                        },
                        "readTimestamp": "2025-01-07T05:35:04.162Z"
                    }
                ],
                "timeStamp": "2025-01-07T11:05:04.162",
                "seen": True
            }
        ],
        "subject": "Message for Medication Understanding",
        "purpose": "Medication Refills",
        "participants": ["Ontada Test1", "Paul Watkins, MD"],
        "status": "CLOSED",
        "conversationId": "cb37190c-10e4-4357-888d-87c7df0d1303"
    },
    {
        "messageResponse": [
            {
                "messageId": "d7d71b8f-dd1f-4a15-954f-e031a04e0aca",
                "messageType": "OUTGOING",
                "content": "Message for Medication Refills",
                "senderName": "Ajayyyy",
                "readBy": [
                    {
                        "readUser": {
                            "type": "Patient",
                            "identifier": "F8C4AF9A56204EB681AF1F7BF9D386CF",
                            "displayName": "watson_james@yopmail.com",
                            "firstName": "Ajayyyy",
                            "lastName": "kase Brewerr",
                            "patientPortalId": "13040a60-e403-45ae-8a99-5b6cb0c40daa"
                        },
                        "readTimestamp": "2025-11-20T05:37:27.531Z"
                    }
                ],
                "timeStamp": "2025-11-20T11:07:27.532",
                "seen": True,
                "attachments": []
            }
        ],
        "subject": "Message for Medication Understanding",
        "purpose": "Medication Refills",
        "participants": ["Paul Watkins, MD"],
        "status": "CLOSED",
        "conversationId": "3671a3be-2ffe-4dde-b1e4-81cefb81f56d"
    }
]
