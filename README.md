# Message App

A full-stack messaging application with a FastAPI backend (supporting semantic and keyword search) and a React + Vite frontend. The project is organized into three main folders: `backend`, `frontend`, and `shared`.

---

## Table of Contents

- Features
- Project Structure
- Backend Setup
- Frontend Setup
- Shared Data & Scripts
- Development Workflow
- License

---

## Features

- FastAPI-based REST API backend
- Semantic and keyword search over messages (FAISS + sentence-transformers)
- Modern React frontend (Vite)
- Shared mock data and scripts for development

---

## Project Structure

```
message-app/
├── backend/      # FastAPI API server (semantic + keyword search)
├── frontend/     # React + Vite client
├── shared/       # Shared data and scripts
└── README.md     # Project documentation
```

---

## Backend Setup

1. Navigate to the backend folder:
   ```sh
   cd backend
   ```
2. (Recommended) Create a virtual environment:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # Or: source .venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Build the FAISS index (required for semantic search):
   ```sh
   python -m app.build_index
   ```
   This will process the shared message data and create the FAISS index in `../shared/data/`.
5. Start the FastAPI server:
   ```sh
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at [http://localhost:8000](http://localhost:8000)

---

## Backend API Endpoints

- `GET /api/messages` — Get all messages
- `POST /api/search` — Keyword search (body: `{ "query": "...", "top_k": 5 }`)
- `POST /api/semantic-search` — Semantic search using embeddings (body: `{ "query": "...", "top_k": 5 }`)

---

## Frontend Setup

1. Navigate to the frontend folder:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the development server:
   ```sh
   npm run dev
   ```
   The frontend will be available at [http://localhost:5173](http://localhost:5173) by default.

---

## Shared Data & Scripts

- `shared/data/`: Contains mock and flattened message data, FAISS index, and metadata for development/testing.
- `shared/scripts/flattenMessages.py`: Script to process/flatten message data.

---

## Development Workflow

- **Backend:** Edit API logic in `backend/app/` and restart the FastAPI server as needed. If you update message data, rebuild the FAISS index.
- **Frontend:** Update UI in `frontend/src/` and hot-reload with Vite.
- **Shared:** Update mock data or scripts in `shared/` as required.

---

## License

MIT License
