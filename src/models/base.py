from abc import ABC, abstractmethod
from dataclasses import dataclass, fields, asdict

from dtos.base import BaseDto


@dataclass(frozen=True)
class Model(ABC):

    @classmethod
    def from_dict(cls, data: dict) -> "Model":
        valid_data = {field.name: data.get(field.name) for field in fields(cls)}
        return cls(**valid_data)

    def to_dict(self, include_none=True) -> dict:
        data = asdict(self)
        if include_none:
            return data
        return {key: value for key, value in data.items() if value is not None}

    @classmethod
    def get_fields(cls) -> list[str]:
        return [field.name for field in fields(cls)]

    @classmethod
    @abstractmethod
    def from_dto(cls, dto: BaseDto) -> "Model":
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_table_query() -> str:
        raise NotImplementedError
