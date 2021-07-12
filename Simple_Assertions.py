import requests


class TestCookieAssert:
    url = 'https://playground.learnqa.ru/api/homework_cookie'

    def test_cookie_value(self):
        response = requests.get(self.url)
        assert response.cookies['HomeWork'] == 'hw_value', f"Cookies {response.cookies} doesn't equal expected value"
