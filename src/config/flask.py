import os


class FlaskConfig:
    def __init__(self):
        self._config = {
            "DEBUG": True,
            "CACHE_TYPE": "SimpleCache",
            "CACHE_DEFAULT_TIMEOUT": 300,
        }
        self._config.update({"JWT_SECRET_KEY": os.environ.get("JWT_SECRET_KEY")})

    @property
    def get_config(self) -> dict:
        return self._config
