# Message App Backend

Backend for the Message App, built with **FastAPI**. Supports both keyword and semantic search over message data using **FAISS** and **sentence-transformers**.

---

## Features

- FastAPI-based REST API
- CORS enabled for frontend integration
- Keyword and semantic search endpoints
- Extractive conversation summarization endpoint (word frequency-based)
- FAISS vector index for fast semantic search
- Uses Sentence Transformers for embeddings
- Loads and serves messages from shared data
- Modular codebase for easy extension

---

## New in this version

- **Conversation Summarization:**
  - New `/api/summarize` endpoint for extractive summaries and highlights per conversation.
  - Summarization uses word frequency to extract top sentences and highlights.
- **AI Search Toggle:**
  - Frontend can toggle between keyword and semantic (AI) search.
- **Improved Development Workflow:**
  - Updated documentation and code structure for easier extension and testing.

---

## Project Structure

```
backend/
├── app/
│   ├── api.py              # API route definitions
│   ├── build_index.py      # Script to build FAISS index
│   ├── main.py             # FastAPI app entrypoint
│   ├── semantic_search.py  # Semantic search engine logic
│   └── utils.py            # Utilities for loading data
├── requirements.txt        # Python dependencies
├── .python-version         # Python version pin (3.11)
└── README.md               # This file
```

---

## Requirements

- Python 3.11 (see `.python-version`)
- pip

---

## Setup Instructions

1. **Navigate to the backend folder:**

   ```sh
   cd backend
   ```

2. **(Recommended) Create a virtual environment:**

   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # Or: source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Build the FAISS index (required for semantic search):**

   ```sh
   python -m app.build_index
   ```

   This processes the shared message data and creates the FAISS index in `../shared/data/`.

5. **Start the FastAPI server:**
   ```sh
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at [http://localhost:8000](http://localhost:8000)

---

## API Endpoints

- `GET /api/messages` — Get all messages
- `POST /api/search` — Keyword search (body: `{ "query": "...", "top_k": 5 }`)
- `POST /api/semantic-search` — Semantic search using embeddings (body: `{ "query": "...", "top_k": 5 }`)
- `POST /api/summarize` — Extractive conversation summary and highlights (body: `{ "conversationId": "...", "scope": "all"|"last_5" }`)

---

## Notes

- Loads message data from `../shared/data/flattenedMessages.json`.
- Semantic search index is stored in `../shared/data/faiss.index` and `faiss_meta.json`.
- If you see an error about missing FAISS index, run the build step above.
- CORS is enabled for all origins by default (see `main.py`).
- Compiled Python files are stored in `__pycache__/` directories.
- Summarization endpoint returns both a summary and a list of highlights (most frequent keywords).

---

## Development

- Edit API logic in `app/api.py` and `app/semantic_search.py`.
- Add or update summarization logic in `app/api.py` as needed.
- Update or reprocess data in `shared/data/` as needed.
- For frontend integration, see the main project `README.md`.

---

## License

MIT License
