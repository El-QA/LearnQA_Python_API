import allure
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.feature("Create user cases")
class TestUserRegister(BaseCase):

    exclude_parameters = {
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    }

    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_inappropriate_email(self):
        email = 'vinkotov.example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("condition", exclude_parameters)
    def test_create_user_without_one_parameter(self, condition):
        data = self.prepare_registration_data()
        del data[condition]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", \
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data['username'] = self.rand_str(1)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        data['username'] = self.rand_str(251)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", \
            f"Unexpected response content {response.content}"
