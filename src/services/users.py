from typing import Any

from flask_caching import Cache

from dtos.base import BaseDto
from dtos.read_user import ReadUserDto
from dtos.search_user import SearchUserDto
from exceptions.database import UniqueAttributeException, EntityNotFoundException
from models.user import UserModel
from repositories.user import UserRepository
from services.base import BaseService


class UsersService(BaseService):
    def __init__(self, _cache: Cache):
        self._cache = _cache
        super().__init__()
        self._repository = UserRepository()

    def create(self, dto: BaseDto) -> BaseDto:
        self._check_unique_fields(dto)
        created_user_model = self._repository.create(dto)
        return ReadUserDto(**created_user_model.to_dict())

    def read_by_id(self, id: Any) -> BaseDto:
        @self._cache.cached(timeout=60, key_prefix="user_by_id")
        def cached_read_by_id(id: Any) -> BaseDto:
            user_model = self._repository.get_by_id(id)
            if user_model is None:
                raise EntityNotFoundException("id", id)
            return ReadUserDto(**user_model.to_dict())

        return cached_read_by_id(id)

    def read_all(self) -> list[BaseDto]:
        @self._cache.cached(timeout=60, key_prefix="all_users")
        def cached_read_all() -> list[BaseDto]:
            user_models = self._repository.get_all()
            return [ReadUserDto(**user_model.to_dict()) for user_model in user_models]

        return cached_read_all()

    def update(self, id: Any, dto: BaseDto) -> BaseDto:
        user_exists = self._repository.exists_by(SearchUserDto(id=id))
        if not user_exists:
            raise EntityNotFoundException("id", id)
        self._check_unique_fields(dto)
        updated_user_model = self._repository.update(id, dto)
        return ReadUserDto(**updated_user_model.to_dict())

    def delete(self, id: Any) -> BaseDto:
        user_model = self._repository.delete(id)
        if user_model is None:
            raise EntityNotFoundException("id", id)
        return ReadUserDto(**user_model.to_dict())

    def _check_unique_fields(self, dto: BaseDto) -> None:
        dto_data = dto.model_dump()
        unique_fields = UserModel.get_unique_fields()
        for unique_field in unique_fields:
            if dto_data.get(unique_field) is None:
                continue
            if self._repository.exists_by(SearchUserDto(**{unique_field: dto_data[unique_field]})):
                raise UniqueAttributeException(unique_field)
