from typing import Annotated

from pydantic import field_validator, Field, model_validator

from dtos.base_user import BaseUserDto


class UpdateUserDto(BaseUserDto):
    password: Annotated[str | None, Field(default=None, validate_default=True)]
    is_active: Annotated[bool | None, Field(default=None, validate_default=True)]

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

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str | None) -> str | None:
        if password is None:
            return None
        return cls.base_password_validation(password)

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> None:
        values = self.model_dump().values()
        if all([value is None for value in values]):
            raise ValueError("You must provide at least one field")
