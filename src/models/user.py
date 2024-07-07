from dataclasses import dataclass
import datetime

import bcrypt

from dtos.base import BaseDto
from models.base import Model


@dataclass(frozen=True)
class UserModel(Model):
    username: str
    full_name: str
    email: str
    hashed_password: str
    is_active: bool
    created_at: str
    updated_at: str
    id: int | None = None

    @classmethod
    def from_dto(cls, dto: BaseDto, is_creation: bool = True) -> "Model":
        data = dto.model_dump()
        iso_date = datetime.datetime.now().isoformat(sep=" ")
        if "password" in data and data["password"] is not None:
            data["hashed_password"] = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
        data["updated_at"] = iso_date
        if is_creation:
            data["created_at"] = iso_date
            data["is_active"] = True
        return cls.from_dict(data)

    @staticmethod
    def create_table_query() -> str:
        return """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username VARCHAR(25) UNIQUE NOT NULL,
                full_name VARCHAR(50) NOT NULL,
                email VARCHAR(50) UNIQUE NOT NULL,
                hashed_password VARCHAR(60) UNIQUE NOT NULL,
                is_active BOOLEAN NOT NULL,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            );
        """

    @staticmethod
    def get_unique_fields() -> list[str]:
        return ["username", "email"]
