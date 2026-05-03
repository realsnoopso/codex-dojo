from fastapi import FastAPI

from src.routes import router as api_router


app: FastAPI = FastAPI(title="Codex Dojo API", version="0.1.0")
app.include_router(api_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to Codex Dojo API"}

