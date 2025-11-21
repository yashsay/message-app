#!/usr/bin/env python3
"""
Quick Start Script for Testing Bulk Update API

This script demonstrates the complete workflow of the bulk update endpoint.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from example_data import EXAMPLE_CONVERSATIONS


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def main():
    """Main testing workflow."""

    print_section("Bulk Update API - Quick Start Guide")

    print("\n📋 This script will help you test the bulk update endpoint.")
    print("\n1️⃣  First, make sure the FastAPI server is running:")
    print("    cd backend")
    print("    uvicorn app.main:app --reload")

    print("\n2️⃣  The server should be accessible at:")
    print("    http://localhost:8000")

    print("\n3️⃣  Test the endpoint using one of these methods:")

    print_section("Method 1: Using Python requests")
    print("""
import requests
from example_data import EXAMPLE_CONVERSATIONS

response = requests.post(
    "http://localhost:8000/api/bulk-update",
    json=EXAMPLE_CONVERSATIONS
)
print(response.json())
    """)

    print_section("Method 2: Using cURL")
    print("""
# Save example data to file first
python -c "import json; from example_data import EXAMPLE_CONVERSATIONS; \\
    json.dump(EXAMPLE_CONVERSATIONS, open('request.json', 'w'), indent=2)"

# Then make the request
curl -X POST http://localhost:8000/api/bulk-update \\
  -H "Content-Type: application/json" \\
  -d @request.json
    """)

    print_section("Method 3: Using test script")
    print("""
python test_bulk_update.py
    """)

    print_section("Example Request Data")
    print(f"\nNumber of conversations: {len(EXAMPLE_CONVERSATIONS)}")
    for idx, conv in enumerate(EXAMPLE_CONVERSATIONS, 1):
        print(f"\nConversation {idx}:")
        print(f"  ID: {conv['conversationId']}")
        print(f"  Subject: {conv['subject']}")
        print(f"  Status: {conv['status']}")
        print(f"  Messages: {len(conv['messageResponse'])}")

    print_section("Expected Response Format")
    print("""
{
  "success": true,
  "message": "Conversations updated successfully",
  "conversationsProcessed": 2,
  "conversationsAdded": 1,
  "conversationsUpdated": 1,
  "messagesAdded": 5
}
    """)

    print_section("API Workflow")
    print("""
1. Load mockMessages.json
2. Process each conversation:
   - Check if conversationId exists
   - Add new conversation OR merge messages
3. Save updated mockMessages.json
4. Run flattenMessages.py
5. Rebuild FAISS index
6. Return statistics
    """)

    print_section("Documentation")
    print("\n📖 Full API documentation: backend/BULK_UPDATE_API.md")
    print("📊 Implementation details: backend/IMPLEMENTATION_SUMMARY.md")
    print("🧪 Test script: backend/test_bulk_update.py")
    print("📝 Example data: backend/example_data.py")

    print_section("Interactive Mode")
    response = input("\n🚀 Would you like to save the example data to a JSON file? (y/n): ")

    if response.lower() == 'y':
        output_file = "example_request.json"
        with open(output_file, 'w') as f:
            json.dump(EXAMPLE_CONVERSATIONS, f, indent=2)
        print(f"\n✅ Saved example data to: {output_file}")
        print(f"\n📤 You can now use this file with cURL:")
        print(f"    curl -X POST http://localhost:8000/api/bulk-update \\")
        print(f"      -H \"Content-Type: application/json\" \\")
        print(f"      -d @{output_file}")

    print("\n✨ Ready to test! Make sure the server is running first.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
