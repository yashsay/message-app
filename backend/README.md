# Message App Backend

Backend for the Message App, built with **FastAPI**. Supports both keyword and semantic search over message data using **FAISS** and **sentence-transformers**.

---

## Features

- **FastAPI-based REST API** with automatic OpenAPI documentation
- **CORS enabled** for seamless frontend integration
- **Dual search capabilities**: keyword and semantic search endpoints
- **Conversation summarization**: extractive summaries with keyword highlights
- **FAISS vector indexing** for high-performance semantic search
- **Sentence Transformers**: state-of-the-art embeddings for semantic understanding
- **Shared data integration**: loads and serves messages from centralized data store
- **Modular architecture**: clean separation of concerns for easy extension and testing
- **Startup validation**: automatic FAISS index loading with error handling

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

## Key Dependencies

- **FastAPI**: Modern web framework for building APIs
- **FAISS**: Facebook AI Similarity Search for vector operations
- **sentence-transformers**: Pre-trained transformer models for embeddings
- **uvicorn**: ASGI server for running FastAPI applications
- **scikit-learn**: Machine learning utilities for text processing
- **torch**: PyTorch for deep learning model support

---

## Requirements

- **Python 3.11.9** (see `.python-version`)
- pip
- Virtual environment (recommended)

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

### Code Structure

- **API logic**: Edit routes and request handling in `app/api.py`
- **Search engine**: Modify semantic search logic in `app/semantic_search.py`
- **Data utilities**: Update data loading functions in `app/utils.py`
- **Index building**: Modify FAISS index creation in `app/build_index.py`
- **App configuration**: Update CORS, middleware in `app/main.py`

### Common Development Tasks

- **Adding new endpoints**: Define routes in `app/api.py` and update router
- **Updating search logic**: Modify algorithms in `app/semantic_search.py`
- **Data reprocessing**: Update `shared/scripts/flattenMessages.py` then rebuild index
- **Testing changes**: Use FastAPI's automatic docs at `http://localhost:8000/docs`

### Troubleshooting

- **FAISS index errors**: Ensure you've run `python -m app.build_index`
- **Import errors**: Check virtual environment activation and dependencies
- **CORS issues**: Verify frontend URL in `app/main.py` CORS settings
- **Performance issues**: Monitor FAISS index size and consider optimization

### Integration

- **Frontend**: See main project `README.md` for full-stack setup
- **API testing**: Use the interactive docs at `/docs` or `/redoc` endpoints

---

## Performance Considerations

- **FAISS Index Size**: Index size grows with message volume; monitor memory usage
- **Embedding Generation**: First-time startup may be slow due to model loading
- **Concurrent Requests**: FastAPI handles multiple requests efficiently
- **Vector Search**: FAISS provides sub-linear search time complexity

## Production Deployment

- **Environment Variables**: Consider using `.env` for configuration
- **CORS Settings**: Restrict `allow_origins` to specific domains in production
- **Security**: Add authentication/authorization as needed
- **Monitoring**: Implement logging and health check endpoints
- **Scaling**: Consider using multiple workers with `gunicorn`

---

## License

MIT License
