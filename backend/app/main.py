# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router
from app.semantic_search import semantic_engine   # ✅ import your engine

app = FastAPI(title="Message App API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load FAISS index on startup
@app.on_event("startup")
def load_faiss_index():
    try:
        semantic_engine.load_index()
        print("✅ FAISS index loaded successfully")
    except Exception as e:
        print(f"⚠️ Could not load FAISS index: {e}")
        print("👉 Run `python -m app.build_index` first to generate the index.")

# Register API routes
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
