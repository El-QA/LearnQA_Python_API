import requests


class TestCookieAssert:
    url = 'https://playground.learnqa.ru/api/homework_cookie'

    def test_cookie_value(self):
        response = requests.get(self.url)
        assert response.cookies['HomeWork'] == 'hw_value', f"Cookies {response.cookies} doesn't equal expected value"


class TestHeaderAssert:
    url = 'https://playground.learnqa.ru/api/homework_header'

    def test_header_value(self):
        response = requests.get(self.url)
        assert response.headers['Content-Type'] == 'application/json', \
            f"Content-Type {response.headers['Content-Type']} doesn't equal expected value"
        assert response.headers['Content-Length'] == '15', \
            f"Content-Length {response.headers['Content-Length']} doesn't equal expected value"
        assert response.headers['Connection'] == 'keep-alive', \
            f"Connection {response.headers['Connection']} doesn't equal expected value"
        assert response.headers['Keep-Alive'] == 'timeout=10', \
            f"Keep-Alive {response.headers['Keep-Alive']} doesn't equal expected value"
        assert response.headers['Server'] == 'Apache', \
            f"Server {response.headers['Server']} doesn't equal expected value"
        assert response.headers['x-secret-homework-header'] == 'Some secret value', \
            f"x-secret-homework-header {response.headers['x-secret-homework-header']} doesn't equal expected value"
        assert response.headers['Cache-Control'] == 'max-age=0', \
            f"Cache-Control {response.headers['Cache-Control']} doesn't equal expected value"
