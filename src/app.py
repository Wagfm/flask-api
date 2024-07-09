from flask import Flask
from flask_caching import Cache

from config.flask import FlaskConfig
from controllers.users import UsersController
from routes.base import BaseRoute
from routes.root import RootRoute


class FlaskAppWrapper(Flask):
    _instance = None
    _cache = None

    def __init__(self):
        super().__init__(__name__, static_url_path="/api/v1")
        self.config.update(FlaskConfig().get_config)
        self._cache = Cache(self)
        controller = UsersController(self._cache)
        root_route = RootRoute()
        root_route.register_blueprint(BaseRoute("users_route", controller), url_prefix="/users")
        self.register_blueprint(root_route)

    @staticmethod
    def get_instance() -> Flask:
        if FlaskAppWrapper._instance is None:
            _instance = FlaskAppWrapper()
        return FlaskAppWrapper._instance

    @property
    def get_cache(self):
        return self._cache

    def start_server(self):
        self.run("0.0.0.0", debug=True)


if __name__ == '__main__':
    wrapper = FlaskAppWrapper()
    wrapper.start_server()
