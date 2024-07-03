import re
from abc import ABC, abstractmethod
from typing import Annotated

from pydantic import field_validator, Field

from dtos.base import BaseDto


class BaseUserDto(ABC, BaseDto):
    username: Annotated[str | None, Field(default=None, validate_default=True)]
    email: Annotated[str | None, Field(default=None, validate_default=True)]
    full_name: Annotated[str | None, Field(default=None, validate_default=True)]

    @field_validator("username")
    @classmethod
    @abstractmethod
    def validate_username(cls, username: str | None) -> str | None:
        raise NotImplementedError

    @field_validator("email")
    @classmethod
    @abstractmethod
    def validate_email(cls, email: str | None) -> str | None:
        raise NotImplementedError

    @field_validator("full_name")
    @classmethod
    @abstractmethod
    def validate_full_name(cls, full_name: str | None) -> str | None:
        raise NotImplementedError

    @staticmethod
    def base_username_validation(username: str) -> str:
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(username) > 25:
            raise ValueError("Username must be less than 15 characters")
        return username

    @staticmethod
    def base_email_validation(email: str) -> str:
        if not re.match("^(?![0-9 !.]).*@.*", email):
            raise ValueError("Invalid email format. Acceptable pattern is foo.bar@mail.xyz")
        return email

    @staticmethod
    def base_full_name_validation(full_name: str) -> str:
        if len(full_name) < 3:
            raise ValueError("Full name must be at least 3 characters")
        if len(full_name) > 50:
            raise ValueError("Full name must be less than 50 characters")
        return full_name

    @staticmethod
    def base_password_validation(password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(password) > 100:
            raise ValueError("Password too long! The max is 100 characters")
        return password
