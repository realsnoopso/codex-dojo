"""Root route definitions for the API."""

from fastapi import APIRouter

router: APIRouter = APIRouter(tags=["root"])


@router.get("/")
def root() -> dict[str, str]:
    """Return the API welcome message."""
    return {"message": "Welcome to Codex Dojo API"}
