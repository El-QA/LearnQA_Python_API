import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# 1) создавал задачу
response = requests.get(url)
my_token = response.json()['token']
timer = response.json()['seconds']
# 2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
response = requests.get(url, params={'token': my_token})

status = response.json()['status']
if status == 'Job is NOT ready':
    # 3) ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
    time.sleep(timer)
    # 4) делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля result
    response = requests.get(url, params={'token': my_token})
    status = response.json()['status']
    result = response.json()['result']
    if status == 'Job is ready' and result is not None:
        print('Test passed')
