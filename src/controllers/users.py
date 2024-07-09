from typing import Any

from flask import Response, request
from flask_caching import Cache

from controllers.base import BaseController
from dtos.create_user import CreateUserDto
from dtos.update_user import UpdateUserDto
from exceptions.database import EntityNotFoundException
from services.users import UsersService


class UsersController(BaseController):

    def __init__(self, _cache: Cache):
        super().__init__()
        self._service = UsersService(_cache)

    def create(self) -> Response:
        desired_user_data = request.json
        try:
            create_user_dto = CreateUserDto(**desired_user_data)
            read_user_dto = self._service.create(create_user_dto)
        except ValueError as error:
            return self.build_json_response({"message": str(error)}, 400)
        except Exception as exception:
            return self.build_json_response({"message": str(exception)}, 422)
        return self.build_json_response({"user": read_user_dto.model_dump()}, 201)

    def read_by_id(self, id: Any) -> Response:
        try:
            read_user_dto = self._service.read_by_id(id)
        except EntityNotFoundException as exception:
            return self.build_json_response({"message": str(exception)}, 404)
        except Exception as exception:
            return self.build_json_response({"message": str(exception)}, 500)
        return self.build_json_response({"user": read_user_dto.model_dump()}, 200)

    def read_all(self) -> Response:
        try:
            read_user_dtos = self._service.read_all()
        except Exception as exception:
            return self.build_json_response({"message": str(exception)}, 500)
        return self.build_json_response(
            {"users": [dto.model_dump() for dto in read_user_dtos]}, 200
        )

    def update(self, id: Any) -> Response:
        data_to_update = request.json
        try:
            create_user_dto = UpdateUserDto(**data_to_update)
            read_user_dto = self._service.update(id, create_user_dto)
        except ValueError as error:
            return self.build_json_response({"message": str(error)}, 400)
        except EntityNotFoundException as exception:
            return self.build_json_response({"message": str(exception)}, 404)
        except Exception as exception:
            return self.build_json_response({"message": str(exception)}, 422)
        return self.build_json_response({"user": read_user_dto.model_dump()}, 200)

    def delete(self, id: Any) -> Response:
        try:
            deleted_user_dto = self._service.delete(id)
        except EntityNotFoundException as exception:
            return self.build_json_response({"message": str(exception)}, 404)
        except Exception as exception:
            return self.build_json_response({"message": str(exception)}, 500)
        return self.build_json_response({"user": deleted_user_dto.model_dump()}, 200)
