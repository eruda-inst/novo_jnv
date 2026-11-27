from typing import Annotated, Final

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from noname.v1 import config, database, models

security = HTTPBearer()


_SECRET_KEY: Final[str] = config.settings.jwt_secret_key.get_secret_value()
_ALGORITHM: Final[str] = config.settings.jwt_algorithm


async def get_current_user(
    db: Annotated[AsyncSession, Depends(database.get_db)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> models.UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou expiradas.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    access_token = credentials.credentials
    try:
        payload = jwt.decode(jwt=access_token, key=_SECRET_KEY, algorithms=[_ALGORITHM])
    except jwt.InvalidTokenError:
        raise credentials_exception

    token_type = payload.get("type")
    jti = payload.get("jti")
    sub = payload.get("sub")

    if token_type != "access" or not jti or not sub:
        raise credentials_exception

    revoked_token = await db.get(models.RevokedAccessTokenModel, jti)
    if revoked_token is not None:
        raise credentials_exception

    stmt = select(models.UserModel).where(models.UserModel.email == sub)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user
