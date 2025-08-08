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
for group in data:
    for conv in group["data"]:
        for msg in conv["messages"]:
            flattened.append({
                "conversationId": conv["id"],
                "subject": conv.get("subject", ""),
                "sender": msg["sender"],
                "text": msg["text"],
                "timestamp": msg["timestamp"]
            })

# Save to output file
with open(output_path, "w") as f:
    json.dump(flattened, f, indent=2)

print(f"✅ Flattened {len(flattened)} messages to {output_path}")
