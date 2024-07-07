from abc import ABC, abstractmethod
from typing import Any

from dtos.base import BaseDto


class BaseService(ABC):
    @abstractmethod
    def create(self, dto: BaseDto) -> BaseDto:
        raise NotImplementedError

    @abstractmethod
    def read_by_id(self, id: Any) -> BaseDto:
        raise NotImplementedError

    @abstractmethod
    def read_all(self) -> list[BaseDto]:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: Any, dto: BaseDto) -> BaseDto:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: Any) -> BaseDto:
        raise NotImplementedError
