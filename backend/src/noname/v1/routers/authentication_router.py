from typing import Annotated

from fastapi import APIRouter, Depends

from noname.v1 import dependencies, models, schemas

authentication_router = APIRouter(prefix="/authentication", tags=["Authentication"])

CurrentUserDependency = Annotated[
    models.UserModel, Depends(dependencies.get_current_user)
]


@authentication_router.get(path="/me", summary="Retrieve current authenticated user.")
async def me(current_user: CurrentUserDependency) -> schemas.UserOutSchema:
    """
    Return the profile data of the currently authenticated user.
    """
    return schemas.UserOutSchema.model_validate(current_user)
