import datetime
import os
import sqlite3
from typing import Any

from dtos.base import BaseDto
from models.base import Model
from models.user import UserModel
from repositories.base import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self, database_path: str = "/home/wagner/.databases/flask-api-dev.db"):
        super().__init__()
        self._DATABASE_PATH = database_path

        @self._connect
        def setup_table(cursor: sqlite3.Cursor) -> None:
            create_table_query = UserModel.create_table_query()
            cursor.execute(create_table_query)

        setup_table()

    def create(self, dto: BaseDto) -> Model | None:
        desired_model = UserModel.from_dto(dto)
        desired_data = desired_model.to_dict(False)
        columns = [column_name for column_name in desired_data]
        values = [desired_data[column_name] for column_name in columns]
        params = ["?"] * len(values)

        @self._connect
        def create_user(cursor: sqlite3.Cursor) -> Model | None:
            create_user_query = f"""
                INSERT INTO users ({str.join(", ", columns)}) VALUES ({str.join(", ", params)}) RETURNING *;
            """
            cursor = cursor.execute(create_user_query, values)
            item = cursor.fetchone()
            if item is None:
                return None
            return UserModel(**item)

        return create_user()

    def get_by_id(self, id: Any) -> Model | None:
        @self._connect
        def get_user_by_id(cursor: sqlite3.Cursor) -> Model | None:
            get_by_id_query = """
                SELECT * FROM users WHERE id = ?;
            """
            cursor = cursor.execute(get_by_id_query, (id,))
            item = cursor.fetchone()
            if item is None:
                return None
            return UserModel(**item)

        return get_user_by_id()

    def get_by_attrs(self, dto: BaseDto) -> Model | None:
        search_data = dto.model_dump(exclude_none=True)
        column_names = [column_name for column_name in search_data]
        values = [search_data[column_name] for column_name in column_names]
        query_conditions = [f"{column} = ?" for column in column_names]

        @self._connect
        def get_user_by_attr(cursor: sqlite3.Cursor) -> Model | None:
            get_by_id_query = f"""
                SELECT * FROM users WHERE {str.join(" AND ", query_conditions)};
            """
            cursor = cursor.execute(get_by_id_query, (*values,))
            item = cursor.fetchone()
            if item is None:
                return None
            return UserModel(**item)

        return get_user_by_attr()

    def exists_by(self, dto: BaseDto) -> bool:
        search_data = dto.model_dump(exclude_none=True)
        column_names = [column_name for column_name in search_data]
        values = [search_data[column_name] for column_name in column_names]
        query_conditions = [f"{column} = ?" for column in column_names]

        @self._connect
        def exists_by(cursor: sqlite3.Cursor) -> bool:
            exists_by_query = f"""
                SELECT * FROM users WHERE {str.join(" AND ", query_conditions)};
            """
            cursor = cursor.execute(exists_by_query, (*values,))
            return cursor.fetchone() is not None

        return exists_by()

    def get_all(self) -> list[Model]:
        @self._connect
        def get_all_users(cursor: sqlite3.Cursor) -> list[Model]:
            get_by_id_query = """
                SELECT * FROM users;
            """
            cursor = cursor.execute(get_by_id_query)
            items = cursor.fetchall()
            return [UserModel(**item) for item in items]

        return get_all_users()

    def update(self, id: Any, dto: BaseDto) -> Model | None:
        @self._connect
        def update_user(cursor: sqlite3.Cursor) -> Model | None:
            update_data = UserModel.from_dto(dto, False).to_dict()
            columns_to_update = [column for column, value in update_data.items() if value is not None]
            updated_values = [update_data[column] for column in columns_to_update]
            update_query_values = [f"{column} = ?" for column in columns_to_update]
            iso_date = datetime.datetime.now().isoformat(sep=" ")
            update_query = f"""
                UPDATE users SET {str.join(", ", update_query_values)}, updated_at = ? WHERE id = ? RETURNING *;
            """
            cursor = cursor.execute(update_query, (*updated_values, iso_date, id))
            item = cursor.fetchone()
            if item is None:
                return None
            return UserModel(**item)

        return update_user()

    def delete(self, id: Any) -> Model | None:
        @self._connect
        def delete_user_by_id(cursor: sqlite3.Cursor) -> Model | None:
            delete_by_id_query = """
                DELETE FROM users WHERE id = ? RETURNING *;
            """
            cursor = cursor.execute(delete_by_id_query, (id,))
            item = cursor.fetchone()
            if item is None:
                return None
            return UserModel(**item)

        return delete_user_by_id()

    def clear_table(self) -> None:
        @self._connect
        def clear_table(cursor: sqlite3.Cursor) -> None:
            cursor.execute(f"DELETE FROM users;")

        clear_table()

    def _connect(self, function):

        def _db_connect(*args, **kwargs):
            connection = sqlite3.connect(self._DATABASE_PATH)
            try:
                cursor = connection.cursor()
                cursor.row_factory = self._dict_factory
                result = function(cursor, *args, **kwargs)
                connection.commit()
                connection.close()
            except Exception as exception:
                connection.rollback()
                raise exception
            finally:
                connection.close()
            return result

        return _db_connect

    @staticmethod
    def _dict_factory(cursor: sqlite3.Cursor, row: tuple):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}
