import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core import settings

basic_auth = HTTPBasic()


async def require_basic_auth(
    credentials: HTTPBasicCredentials = Depends(basic_auth),
) -> str:
    correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"),
        settings.basic_auth_username,
    )
    correct_password = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        settings.basic_auth_password,
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
