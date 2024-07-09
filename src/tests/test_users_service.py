import unittest

from app import FlaskAppWrapper
from dtos.create_user import CreateUserDto
from dtos.update_user import UpdateUserDto
from exceptions.database import UniqueAttributeException, EntityNotFoundException
from repositories.user import UserRepository
from services.users import UsersService


class TestUsersService(unittest.TestCase):
    def setUp(self):
        self._app = FlaskAppWrapper()
        self._service = UsersService(self._app.get_cache)
        self._userRepository = UserRepository()

    def tearDown(self):
        self._service = None
        self._userRepository.clear_table()

    def test_add_user(self):
        dto = self._get_test_user_()
        created_user_dto = self._service.create(dto)
        self.assertIsNotNone(created_user_dto)
        self.assertEqual(dto.username, created_user_dto.username)
        self.assertRaises(UniqueAttributeException, self._service.create, dto)

    def test_read_user(self):
        dto = self._get_test_user_()
        created_user_dto = self._service.create(dto)
        self.assertEqual(created_user_dto, self._service.read_by_id(1))
        self.assertEqual(created_user_dto, self._service.read_all()[0])

    def test_update_user(self):
        dto = self._get_test_user_()
        created_user_dto = self._service.create(dto)
        update_user_dto = UpdateUserDto(username="wagfmac")
        updated_user_dto = self._service.update(1, update_user_dto)
        self.assertNotEqual(created_user_dto, updated_user_dto)
        self.assertRaises(UniqueAttributeException, self._service.update, 1, UpdateUserDto(username="wagfmac"))
        self.assertRaises(UniqueAttributeException, self._service.update, 1, UpdateUserDto(email="wagfm@mail.com"))
        self.assertRaises(EntityNotFoundException, self._service.update, 2, UpdateUserDto(username="wagfmac"))

    def test_delete_user(self):
        dto = self._get_test_user_()
        created_user_dto = self._service.create(dto)
        read_user_dto = self._service.read_by_id(1)
        deleted_user_dto = self._service.delete(1)
        self.assertEqual(deleted_user_dto, read_user_dto, created_user_dto)
        self.assertRaises(EntityNotFoundException, self._service.delete, 1)

    @staticmethod
    def _get_test_user_() -> CreateUserDto:
        test_user_data = {
            "username": "wagfm",
            "email": "wagfm@mail.com",
            "password": "12345678",
            "full_name": "Wagner Maciel"
        }
        return CreateUserDto(**test_user_data)

    @staticmethod
    def _get_invalid_user() -> CreateUserDto:
        test_user_data = {
            "username": "",
            "email": "wagfm@mail",
            "password": "",
        }
        return CreateUserDto(**test_user_data)
