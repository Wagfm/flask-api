from flask import Blueprint

from controllers.base import BaseController


class BaseRoute(Blueprint):
    def __init__(self, name: str, controller: BaseController):
        super().__init__(name, __name__)
        self.get("/")(controller.read_all)
        self.get("/<int:id>")(controller.read_by_id)
        self.post("/")(controller.create)
        self.patch("/<int:id>")(controller.update)
        self.delete("/<int:id>")(controller.delete)
