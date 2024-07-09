from pydantic import field_validator

from dtos.base import BaseDto
from dtos.base_user import BaseUserDto


class LoginDto(BaseDto):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str) -> str:
        BaseUserDto.base_email_validation(email)
        return email

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        BaseUserDto.base_password_validation(password)
        return password
