from abc import ABC, abstractmethod
from typing import Any

from dtos.base import BaseDto
from models.base import Model


class BaseRepository(ABC):

    @abstractmethod
    def create(self, dto: BaseDto) -> Model:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: Any) -> Model:
        raise NotImplementedError

    @abstractmethod
    def get_by_attrs(self, dto: BaseDto) -> Model:
        raise NotImplementedError

    @abstractmethod
    def exists_by(self, dto: BaseDto) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Model]:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: Any, dto: BaseDto) -> Model:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: Any) -> Model:
        raise NotImplementedError
