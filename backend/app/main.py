"""
Message App API - Main Application Entry Point

This module initializes and configures the FastAPI application for the Message App,
including CORS middleware, semantic search engine initialization, and API route registration.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router as api_router
from app.semantic_search import semantic_engine


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Initialize FastAPI application with metadata
    app = FastAPI(
        title="Message App API",
        version="1.0.0",
        description="API for semantic search and message management",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configure CORS middleware to allow frontend communication
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Replace with specific origins in production
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    return app


# Create the FastAPI application instance
app = create_app()


@app.on_event("startup")
async def startup_event() -> None:
    """
    Application startup event handler.

    Initializes the FAISS semantic search index on application startup.
    If the index fails to load, the application will continue to run but
    semantic search functionality will be unavailable.
    """
    try:
        semantic_engine.load_index()
        print("✅ FAISS semantic search index loaded successfully")
    except Exception as e:
        print(f"⚠️ Failed to load FAISS index: {e}")
        print("💡 To fix this, run: python -m app.build_index")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Application shutdown event handler.

    Performs cleanup operations when the application is shutting down.
    """
    print("🔄 Shutting down Message App API...")


# Register API routes with '/api' prefix
app.include_router(api_router, prefix="/api", tags=["API"])


@app.get("/", tags=["Health"])
async def root() -> dict[str, str]:
    """
    Root endpoint for API health check.

    Returns:
        dict: Basic API information and status
    """
    return {
        "message": "Message App API is running",
        "status": "healthy",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint for monitoring and load balancers.

    Returns:
        dict: Application health status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    # Development server configuration
    # In production, use a WSGI server like Gunicorn instead
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
