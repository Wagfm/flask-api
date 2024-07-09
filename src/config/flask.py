class FlaskConfig:
    def __init__(self):
        self._config = {
            "DEBUG": True,
            "CACHE_TYPE": "SimpleCache",
            "CACHE_DEFAULT_TIMEOUT": 300,
        }

    @property
    def get_config(self) -> dict:
        return self._config
