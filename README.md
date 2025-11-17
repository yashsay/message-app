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

- **FastAPI-based REST API backend** with CORS support
- **Semantic and keyword search** over messages using FAISS and sentence-transformers
- **Conversation summarization** with extractive summaries and keyword highlights
- **Modern React frontend** built with Vite and SCSS styling
- **Advanced search toggle** - switch between keyword and AI-powered semantic search
- **Conversation grouping** - messages organized by conversation with individual summaries
- **Shared mock data and scripts** for development and testing
- **FAISS vector indexing** for fast semantic search performance

---

## Project Structure

```
message-app/
├── backend/                 # FastAPI API server (semantic + keyword search)
│   ├── app/
│   │   ├── api.py          # API route definitions
│   │   ├── build_index.py  # Script to build FAISS index
│   │   ├── main.py         # FastAPI app entrypoint
│   │   ├── semantic_search.py # Semantic search engine logic
│   │   └── utils.py        # Utilities for loading data
│   ├── requirements.txt    # Python dependencies
│   ├── .python-version     # Python version pin (3.11.9)
│   └── README.md           # Backend documentation
├── frontend/               # React + Vite client
│   ├── src/
│   │   ├── components/     # React components (MessageList, Header, DarkVeil)
│   │   ├── styles/         # SCSS theme and styling
│   │   ├── App.jsx         # Main App component
│   │   └── main.jsx        # React entrypoint
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   ├── vite.config.js      # Vite configuration
│   └── README.md           # Frontend documentation
├── shared/                 # Shared data and scripts
│   ├── data/               # Mock data, FAISS index, and metadata
│   │   ├── mockMessages.json       # Original mock message data
│   │   ├── flattenedMessages.json  # Processed message data
│   │   ├── faiss.index            # FAISS vector index
│   │   └── faiss_meta.json        # Index metadata
│   └── scripts/
│       └── flattenMessages.py     # Data processing script
└── README.md               # Project documentation
```

---

## Backend Setup

### Requirements

- **Python 3.11.9** (see `backend/.python-version`)
- pip
- Virtual environment (recommended)

### Setup Instructions

1. Navigate to the backend folder:

   ```sh
   cd backend
   ```

2. **(Recommended) Create a virtual environment:**

   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # Or: source .venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. **Build the FAISS index (required for semantic search):**

   ```sh
   python -m app.build_index
   ```

   This will process the shared message data and create the FAISS index in `../shared/data/`.

5. Start the FastAPI server:
   ```sh
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at [http://localhost:8000](http://localhost:8000)

### Backend API Endpoints

- `GET /api/messages` — Get all messages
- `POST /api/search` — Keyword search (body: `{ "query": "...", "top_k": 5 }`)
- `POST /api/semantic-search` — Semantic search using embeddings (body: `{ "query": "...", "top_k": 5 }`)
- `POST /api/summarize` — Extractive conversation summary and highlights (body: `{ "conversationId": "...", "scope": "all"|"last_5" }`)

---

## Frontend Setup

### Requirements

- **Node.js** (v16 or higher recommended)
- npm or yarn

### Setup Instructions

1. Navigate to the frontend folder:

   ```sh
   cd frontend
   ```

2. Install dependencies:

   ```sh
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```sh
   npm run dev
   # or
   yarn dev
   ```
   The frontend will be available at [http://localhost:5173](http://localhost:5173) by default.

### Build for Production

To build the app for production:

```sh
npm run build
# or
yarn build
```

The output will be in the `dist` folder.

### Frontend Features

- **Advanced Search Toggle** - Switch between keyword and AI-powered semantic search
- **Conversation Grouping** - Messages organized by conversation ID
- **Real-time Summarization** - Generate extractive summaries for any conversation
- **Responsive Design** - Built with SCSS and modern styling
- **Dark Theme** - Includes DarkVeil component with atmospheric effects

---

## Shared Data & Scripts

The `shared` folder contains common data and utilities used by both backend and frontend:

### Data Files

- **`mockMessages.json`** - Original mock message data structure
- **`flattenedMessages.json`** - Processed flat structure for API consumption
- **`faiss.index`** - FAISS vector index for semantic search
- **`faiss_meta.json`** - Metadata for the FAISS index

### Scripts

- **`flattenMessages.py`** - Processes mock data into flattened structure for easier consumption

### Data Processing

To reprocess the mock data:

```sh
cd shared/scripts
python flattenMessages.py
```

This will regenerate `flattenedMessages.json` from `mockMessages.json`. After updating data, remember to rebuild the FAISS index:

```sh
cd backend
python -m app.build_index
```

---

## Development Workflow

### Backend Development

- **Edit API logic** in `backend/app/api.py` and `backend/app/semantic_search.py`
- **Restart the FastAPI server** as needed for changes
- **Update data processing** by modifying `shared/scripts/flattenMessages.py`
- **Rebuild FAISS index** after data changes: `python -m app.build_index`

### Frontend Development

- **Update UI components** in `frontend/src/components/`
- **Modify styling** in `frontend/src/styles/` (SCSS files)
- **Hot-reload automatically** with Vite development server
- **Test API integration** by ensuring backend is running on port 8000

### Data Management

- **Update mock data** in `shared/data/mockMessages.json`
- **Regenerate processed data** with `python shared/scripts/flattenMessages.py`
- **Rebuild search index** with `python -m app.build_index` from backend folder

### Key Technologies

- **Backend**: FastAPI, FAISS, sentence-transformers, uvicorn
- **Frontend**: React 19, Vite, Axios, SCSS
- **Search**: FAISS vector search, keyword filtering
- **Summarization**: Extractive summarization with word frequency analysis

---

## License

MIT License
