import unittest

from dtos.create_user import CreateUserDto
from dtos.search_user import SearchUserDto
from dtos.update_user import UpdateUserDto
from repositories.user import UserRepository


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self._user_repository = UserRepository()
        self._user_repository.clear_table()
        self._test_user_dto = self._get_test_user_()

    def tearDown(self):
        self._user_repository.clear_table()

    def test_add_user(self):
        created_user = self._user_repository.create(self._test_user_dto)
        user_data = created_user.to_dict()
        self.assertEqual(user_data["username"], self._test_user_dto.username)
        self.assertEqual(user_data["full_name"], self._test_user_dto.full_name)
        self.assertEqual(user_data["email"], self._test_user_dto.email)
        self.assertNotEqual(user_data["hashed_password"], self._test_user_dto.password)

    def test_read_user(self):
        self._user_repository.create(self._test_user_dto)
        read_user = self._user_repository.get_by_id(1)
        user_data = read_user.to_dict()
        self.assertEqual(user_data["username"], self._test_user_dto.username)
        self.assertEqual(user_data["full_name"], self._test_user_dto.full_name)
        self.assertEqual(user_data["email"], self._test_user_dto.email)

    def test_exists_by(self):
        self._user_repository.create(self._test_user_dto)
        self.assertFalse(self._user_repository.exists_by(SearchUserDto(full_name="Wagner Silva")))
        self.assertTrue(self._user_repository.exists_by(SearchUserDto(full_name="Wagner Maciel")))
        self.assertTrue(self._user_repository.exists_by(SearchUserDto(email="wagfm@mail.com")))
        self.assertTrue(self._user_repository.exists_by(SearchUserDto(username="wagfm")))

    def test_get_by_attr(self):
        created_user = self._user_repository.create(self._test_user_dto)
        user_data = created_user.to_dict()
        self.assertIsNone(self._user_repository.get_by_attrs(SearchUserDto(full_name="Wagner Silva")))
        self.assertIsNone(self._user_repository.get_by_attrs(SearchUserDto(username="wagfmac")))
        self.assertIsNone(self._user_repository.get_by_attrs(SearchUserDto(email="wagfmac@mail.com")))
        self.assertIsNone(self._user_repository.get_by_attrs(SearchUserDto(full_name="Wagner Silva")))
        self.assertIsNotNone(self._user_repository.get_by_attrs(SearchUserDto(**user_data)))
        self.assertIsNotNone(self._user_repository.get_by_attrs(SearchUserDto(username="wagfm")))
        self.assertIsNotNone(self._user_repository.get_by_attrs(SearchUserDto(full_name="Wagner Maciel")))
        self.assertIsNotNone(self._user_repository.get_by_attrs(SearchUserDto(email="wagfm@mail.com")))
        self.assertIsNotNone(self._user_repository.get_by_attrs(SearchUserDto(username="wagfm")))
        self.assertIsNotNone(self._user_repository.get_by_attrs(
            SearchUserDto(username="wagfm", email="wagfm@mail.com"))
        )
        self._user_repository.get_by_attrs(
            SearchUserDto(username="wagfm", email="wagfm@mail.com", full_name="Wagner Maciel")
        )

    def test_update_user(self):
        dto = self._get_test_user_()
        self._user_repository.create(dto)
        updates = {
            "username": "wagfmac",
            "full_name": "Wagner Silva",
            "email": "wagfmac@mail.com",
            "password": "76543210"
        }
        for key, value in updates.items():
            updated_model = self._user_repository.update(1, UpdateUserDto(**{key: value}))
            if key == "password":
                self.assertNotEqual(value, updated_model.to_dict()["hashed_password"])
                continue
            self.assertEqual(value, updated_model.to_dict()[key])
        self.assertIsNone(self._user_repository.update(2, UpdateUserDto(**updates)))

    def test_delete_user(self):
        created_user = self._user_repository.create(self._test_user_dto)
        self.assertEqual(self._user_repository.delete(1).to_dict(), created_user.to_dict())
        self.assertIsNone(self._user_repository.delete(2))

    @staticmethod
    def _get_test_user_() -> CreateUserDto:
        test_user_data = {
            "username": "wagfm",
            "email": "wagfm@mail.com",
            "password": "12345678",
            "full_name": "Wagner Maciel"
        }
        return CreateUserDto(**test_user_data)
