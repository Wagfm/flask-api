from controllers.users import UsersController
from routes.base import BaseRoute


class UsersRoute(BaseRoute):
    def __init__(self, name: str, controller: UsersController):
        super().__init__(name, controller)
        self.get("/login")(controller.login)
        self.get("/protected")(controller.protected)
