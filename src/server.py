"""Application factory and ASGI app instance."""

from fastapi import FastAPI

from src.routes import router as api_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    fastapi_app: FastAPI = FastAPI(title="Codex Dojo API", version="0.1.0")
    fastapi_app.include_router(api_router)
    return fastapi_app


app: FastAPI = create_app()
