"""FastAPI dependencies for authenticated routes."""

from collections.abc import Callable, Mapping

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.auth.jwt_handler import verify_token
from src.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    """Return the username stored in the bearer token."""
    payload = verify_token(token)
    return str(payload["sub"])


def build_current_user_dependency(
    user_lookup: Callable[[str], Mapping[str, object] | None],
) -> Callable[[str], User]:
    """Build a current-user dependency from an application user lookup."""

    def get_current_user(username: str = Depends(get_current_username)) -> User:
        stored_user = user_lookup(username)
        if stored_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return User.model_validate(stored_user)

    return get_current_user
