import requests
import re

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
method_list = ["GET", "POST", "PUT", "DELETE"]
method_query = {
    "GET":  requests.get(url, params={"method": method_list[0]}),
    "POST": requests.post(url, data={"method": method_list[1]}),
    "PUT": requests.put(url, data={"method": method_list[2]}),
    "DELETE": requests.delete(url, data={"method": method_list[3]})
}

# Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
print('Question 1')

responses_without_method = [requests.get(url), requests.post(url), requests.put(url), requests.delete(url)]
for response in responses_without_method:
    print(f'code: {response.status_code} payload: {response.text}')

# Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
print('Question 2')

wrong_method = requests.head(url)
print(f'code: {wrong_method.status_code}')

# Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
print('Question 3')

for request in method_query:
    response = method_query[request]
    print(f'code: {response.status_code} payload: {response.text}')

# С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее.
# И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок.
print('Question 4')
for method in method_list:
    get_response = requests.get(url, params={"method": method})
    actual_method = re.search("\[(.+?)\]", str(get_response.request))
    if get_response.text == '{"success":"!"}' and actual_method.group(1) != method:
        print(f'expected method: GET but actual method: {method} code: {get_response.status_code} '
              f'payload: {get_response.text}')

    post_response = requests.post(url, data={"method": method})
    actual_method = re.search("\[(.+?)\]", str(post_response.request))
    if post_response.text == '{"success":"!"}' and actual_method.group(1) != method:
        print(f'expected method: POST but actual method: {method} code: {post_response.status_code} '
              f'payload: {post_response.text}')

    put_response = requests.put(url, data={"method": method})
    actual_method = re.search("\[(.+?)\]", str(put_response.request))
    if put_response.text == '{"success":"!"}' and actual_method.group(1) != method:
        print(f'expected method: PUT but actual method: {method} code: {put_response.status_code} '
              f'payload: {put_response.text}')

    delete_response = requests.delete(url, data={"method": method})
    actual_method = re.search("\[(.+?)\]", str(delete_response.request))
    if delete_response.text == '{"success":"!"}' and actual_method.group(1) != method:
        print(f'expected method: DELETE but actual method: {method} code: {delete_response.status_code} '
              f'payload: {delete_response.text}')
