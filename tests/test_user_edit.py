from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_not_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_reg = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_key(response_reg, "id")

        user_id = self.get_json_value(response_reg, "id")

        # EDIT
        new_name = "Changed Name"
        response = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {response.content}"

    def test_edit_auth_as_not_same_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_reg = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_key(response_reg, "id")

        email = register_data['email']
        password = register_data['password']
        user_id_login = self.get_json_value(response_reg, "id")

        # REGISTER ANOTHER
        register_another_data = self.prepare_registration_data()
        response_another_reg = MyRequests.post("/user/", data=register_another_data)

        Assertions.assert_code_status(response_another_reg, 200)

        email_another = register_another_data['email']
        password_another = register_another_data['password']
        user_id = self.get_json_value(response_another_reg, "id")
        assert user_id_login != user_id, "Users have same id"

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 200)

        # LOGIN ANOTHER
        login_data = {
            'email': email_another,
            'password': password_another
        }
        response_login_another = MyRequests.post("/user/login", data=login_data)

        auth_sid_another = self.get_cookie(response_login_another, "auth_sid")
        token_another = self.get_header(response_login_another, "x-csrf-token")

        # GET
        response_info = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token_another},
            cookies={"auth_sid": auth_sid_another}
        )

        Assertions.assert_json_value_by_name(
            response_info,
            "firstName",
            "learnqa",
            "Wrong name of the user after edit"
        )

    def test_edit_user_email_with_inappropriate_value(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_reg = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_key(response_reg, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_reg, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # EDIT
        new_email = "Changed.Name.com"
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    def test_edit_user_name_with_short_value(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_reg = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_key(response_reg, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_reg, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # EDIT
        new_name = self.rand_str(1)
        response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)
        assert response.json()["error"] == "Too short value for field firstName", \
            f"Unexpected response content {response.content}"
