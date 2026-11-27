import datetime as dt
import secrets
import uuid
from typing import Final

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from noname.v1 import config, models, schemas

ph = PasswordHasher()

_DUMMY_HASH: Final[str] = ph.hash(secrets.token_urlsafe(32))
_ACCESS_TOKEN_EXPIRE_MINUTES: Final[PositiveInt] = (
    config.settings.jwt_access_token_expire_minutes
)
_REFRESH_TOKEN_EXPIRE_DAYS: Final[PositiveInt] = (
    config.settings.jwt_refresh_token_expire_days
)
_SECRET_KEY: Final[str] = config.settings.jwt_secret_key.get_secret_value()
_ALGORITHM: Final[str] = config.settings.jwt_algorithm


def _create_token(
    sub: str, type: str, expires_delta: dt.timedelta
) -> tuple[str, str, dt.datetime]:
    now = dt.datetime.now(dt.UTC)
    expires_at = now + expires_delta
    jti = str(uuid.uuid4())
    payload = {
        "sub": sub,
        "type": type,
        "jti": jti,
        "iat": now,
        "exp": expires_at,
    }
    token = jwt.encode(payload=payload, key=_SECRET_KEY, algorithm=_ALGORITHM)
    return token, jti, expires_at


async def login(
    db: AsyncSession, credentials: schemas.CredentialsIn
) -> schemas.TokenOutSchema:
    stmt = select(models.UserModel).where(models.UserModel.email == credentials.email)
    user = (await db.execute(stmt)).scalar_one_or_none()
    password_hash = str(user.password) if user is not None else _DUMMY_HASH

    try:
        ph.verify(hash=password_hash, password=credentials.password)
    except VerifyMismatchError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas."
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas."
        )

    access_token, _, _ = _create_token(
        sub=str(user.email),
        type="access",
        expires_delta=dt.timedelta(minutes=_ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token, refresh_jti, refresh_expires_at = _create_token(
        sub=str(user.email),
        type="refresh",
        expires_delta=dt.timedelta(days=_REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db.add(
        models.ActiveRefreshTokenModel(
            jti=refresh_jti,
            expires_at=refresh_expires_at,
            user_id=user.id,
        )
    )
    await db.commit()

    return schemas.TokenOutSchema(
        access_token=access_token, refresh_token=refresh_token
    )
