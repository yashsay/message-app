import json
import os

# Set paths relative to script location
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "../data/mockMessages.json")
output_path = os.path.join(base_dir, "../data/flattenedMessages.json")

# Load mock messages
with open(input_path, "r") as f:
    data = json.load(f)

flattened = []

# Flatten the nested messages
# New structure: array of conversation objects, each with messageResponse array
for conversation in data:
    conversation_id = conversation.get("conversationId", "unknown")
    subject = conversation.get("subject", "")
    purpose = conversation.get("purpose", "")
    participants = conversation.get("participants", [])

    for msg in conversation.get("messageResponse", []):
        flattened.append({
            "conversationId": conversation_id,
            "subject": subject,
            "purpose": purpose,
            "participants": participants,
            "messageId": msg.get("messageId", ""),
            "messageType": msg.get("messageType", ""),
            "sender": msg.get("senderName", "Unknown"),
            "text": msg.get("content", ""),
            "timestamp": msg.get("timeStamp", ""),
            "seen": msg.get("seen", False),
            "hasAttachments": len(msg.get("attachments", [])) > 0
        })

# Save to output file
with open(output_path, "w") as f:
    json.dump(flattened, f, indent=2)

print(f"✅ Flattened {len(flattened)} messages to {output_path}")
