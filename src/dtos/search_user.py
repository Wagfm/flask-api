from typing import Annotated, Any

from pydantic import field_validator, Field

from dtos.base_user import BaseUserDto


class SearchUserDto(BaseUserDto):
    id: Annotated[Any | None, Field(default=None, validate_default=False)]

    @field_validator("username")
    @classmethod
    def validate_username(cls, username: str | None) -> str | None:
        if username is None:
            return None
        return cls.base_username_validation(username)

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str | None) -> str | None:
        if email is None:
            return None
        return cls.base_email_validation(email)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, full_name: str | None) -> str | None:
        if full_name is None:
            return None
        return cls.base_full_name_validation(full_name)
