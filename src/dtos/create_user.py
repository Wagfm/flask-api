from typing import Annotated

from pydantic import field_validator, Field

from dtos.base_user import BaseUserDto


class CreateUserDto(BaseUserDto):
    password: Annotated[str | None, Field(default=None, validate_default=True)]

    @field_validator("username")
    @classmethod
    def validate_username(cls, username: str | None) -> str | None:
        if username is None:
            raise ValueError("username is required")
        return cls.base_username_validation(username)

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str | None) -> str | None:
        if email is None:
            raise ValueError("email is required")
        return cls.base_email_validation(email)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, full_name: str | None) -> str | None:
        if full_name is None:
            raise ValueError("full_name is required")
        return cls.base_full_name_validation(full_name)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str | None) -> str | None:
        if password is None:
            raise ValueError("password is required")
        return cls.base_password_validation(password)
