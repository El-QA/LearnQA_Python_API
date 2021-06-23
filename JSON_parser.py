import json

source = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
messages = json.loads(source)

main_key = "messages"
key = "message"

if main_key in messages:
    second = messages[main_key][1][key]
    print(second)
else:
    print(f"Key {main_key} wasn't found")
