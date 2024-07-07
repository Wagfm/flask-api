from flask import Blueprint


class RootRoute(Blueprint):
    def __init__(self):
        super().__init__("root", __name__, url_prefix="/api/v1")
