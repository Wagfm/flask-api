class UniqueAttributeException(Exception):
    def __init__(self, attribute_name: str):
        super().__init__(f"Entity with the same {attribute_name} already exists")


class EntityNotFoundException(Exception):
    def __init__(self, column_name: str, value: str):
        super().__init__(f"Entity with {column_name}={value} does not exist")
