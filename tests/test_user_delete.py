import allure
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):

    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_protected_user(self):
        # LOGIN
        date = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_login = MyRequests.post("/user/login", data=date)

        Assertions.assert_code_status(response_login, 200)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # DELETE
        response = MyRequests.delete("/user/2",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response.content}"

        # GET
        response_get = MyRequests.get(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_code_status(response_get, 200)
        Assertions.assert_json_has_keys(response_get, expected_fields)

    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_reg = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_key(response_reg, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_reg, "id")

        # LOGIN
        date = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=date)

        Assertions.assert_code_status(response_login, 200)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # DELETE
        response = MyRequests.delete(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response, 200)

        # GET
        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_get, 404)

    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_as_not_same_user(self):
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
        date = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=date)

        Assertions.assert_code_status(response_login, 200)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # DELETE
        response = MyRequests.delete(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})

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
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_code_status(response_info, 200)
        Assertions.assert_json_has_keys(response_info, expected_fields)
