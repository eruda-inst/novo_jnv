from pydantic import BaseModel, EmailStr, Field, PositiveInt

from noname.v1 import config


class CredentialsIn(BaseModel):
    email: EmailStr = Field(
        description="Registered e-mail address of the user.",
        examples=["email@email.com"],
    )
    password: str = Field(
        min_length=8,
        description="Plain-text password associated with the e-mail address.",
        examples=["12345678"],
    )


class TokenOut(BaseModel):
    expires_in: PositiveInt | None = Field(
        default=config.settings.jwt_token_expire_seconds,
        description="JWT expiration time in seconds.",
        examples=[config.settings.jwt_token_expire_seconds],
    )
    token_type: str | None = Field(
        default="Bearer", description="Type of the JWT token.", examples=["Bearer"]
    )
    access_token: str = Field(
        description="JWT token used to access.", examples=["eyJ..."]
    )
    refresh_token: str = Field(
        description="JWT token used to refresh.", examples=["eyJ..."]
    )
