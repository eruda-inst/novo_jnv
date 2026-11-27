from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from noname.v1 import database, dependencies, models, schemas, services

authentication_router = APIRouter(prefix="/authentication", tags=["Authentication"])

DatabaseDependency = Annotated[AsyncSession, Depends(database.get_db)]
CurrentUserDependency = Annotated[
    models.UserModel, Depends(dependencies.get_current_user)
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
