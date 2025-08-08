# Message App

A full-stack messaging application with a Python Flask backend and a React + Vite frontend. The project is organized into three main folders: `backend`, `frontend`, and `shared`.

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

- Real-time messaging (API-based)
- Modern React frontend (Vite)
- Python Flask backend
- Shared mock data and scripts for development

---

## Project Structure

```
message-app/
├── backend/      # Flask API server
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
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```sh
   python app/main.py
   ```
   The backend will start on the default port (e.g., 5000).

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

- `shared/data/`: Contains mock and flattened message data for development/testing.
- `shared/scripts/flattenMessages.py`: Script to process/flatten message data.

---

## Development Workflow

- **Backend:** Make API changes in `backend/app/` and restart the Flask server as needed.
- **Frontend:** Update UI in `frontend/src/` and hot-reload with Vite.
- **Shared:** Update mock data or scripts in `shared/` as required.

---

## License

This project is licensed under the MIT License.
