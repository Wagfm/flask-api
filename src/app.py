from flask import Flask

from controllers.users import UsersController
from routes.base import BaseRoute
from routes.root import RootRoute


def main() -> None:
    app = Flask(__name__, static_url_path="/api/v1")
    controller = UsersController()
    root_route = RootRoute()
    root_route.register_blueprint(BaseRoute("users_route", controller), url_prefix="/users")
    app.register_blueprint(root_route)
    app.run("127.0.0.1", debug=True)


if __name__ == '__main__':
    main()
