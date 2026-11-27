from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from noname.v1 import database, dependencies, models, schemas, services

authentication_router = APIRouter(prefix="/authentication", tags=["Authentication"])

DatabaseDependency = Annotated[AsyncSession, Depends(database.get_db)]
CurrentUserDependency = Annotated[
    models.UserModel, Depends(dependencies.get_current_user)
]
RefreshToken = Annotated[
    str,
    Body(
        embed=True,
        description="Valid JWT refresh token used to issue new tokens.",
        examples=["eyJ..."],
    ),
]


@authentication_router.get(path="/me", summary="Retrieve current authenticated user.")
async def me(current_user: CurrentUserDependency) -> schemas.UserOutSchema:
    """
    Return the profile data of the currently authenticated user.
    """
    return schemas.UserOutSchema.model_validate(current_user)


@authentication_router.post(
    path="/login", summary="Authenticate user and issue tokens."
)
async def login(
    db: DatabaseDependency, credentials: schemas.CredentialsIn
) -> schemas.TokenOutSchema:
    """
    Validate user credentials and return a new pair of JWT access and refresh tokens.
    """
    return await services.login(db=db, credentials=credentials)


@authentication_router.post(
    path="/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke tokens and end session.",
)
async def logout(
    db: DatabaseDependency,
    current_user: CurrentUserDependency,
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(dependencies.security)
    ],
    refresh_token: RefreshToken,
) -> None:
    """
    Revoke the current access token and invalidate the provided refresh token to end the user session.
    """
    await services.logout(
        db=db,
        access_token=credentials.credentials,
        refresh_token=refresh_token,
        user_id=int(current_user.id),  # type: ignore[arg-type]
    )


@authentication_router.post(
    path="/refresh", summary="Refresh access and refresh tokens."
)
async def refresh(
    db: DatabaseDependency, refresh_token: RefreshToken
) -> schemas.TokenOutSchema:
    """
    Validate an active refresh token, rotate it, and return a new pair of JWT access and refresh tokens.
    """
    return await services.refresh(db=db, refresh_token=refresh_token)
