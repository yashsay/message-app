# backend/app/api.py
from flask import Blueprint, jsonify, request
from app.utils import load_flattened_messages

api_bp = Blueprint("api", __name__)

@api_bp.route("/messages", methods=["GET"])
def get_all_messages():
    messages = load_flattened_messages()
    return jsonify({"messages": messages})

@api_bp.route("/search", methods=["POST"])
def search_messages():
    data = request.get_json()
    query = data.get("query", "").lower()
    messages = load_flattened_messages()

    filtered = [
        msg for msg in messages if query in msg["text"].lower()
    ]
    return jsonify({"results": filtered})
