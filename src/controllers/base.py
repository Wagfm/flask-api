import json
from abc import ABC, abstractmethod
from typing import Any

from flask import Response


class BaseController(ABC):

    @abstractmethod
    def create(self) -> Response:
        raise NotImplementedError

    @abstractmethod
    def read_by_id(self, id: Any) -> Response:
        raise NotImplementedError

    @abstractmethod
    def read_all(self) -> Response:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: Any) -> Response:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: Any) -> Response:
        raise NotImplementedError

    @staticmethod
    def build_json_response(content: dict, status_code: int) -> Response:
        return Response(json.dumps(content), status_code, mimetype="application/json")
