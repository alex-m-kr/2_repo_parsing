'''
1. Посмотреть документацию к API GitHub, разобраться как вывести список
репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
'''
import json
import requests

name = 'alex-m-kr'
url = f'https://api.github.com/users/{name}/repos'

r = requests.get(url)
json_data = r.json()
# print(type(json_data))
# print(json_data)
with open('hw1_1.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f)

for i, el in enumerate(json_data, start=1):
    print(f'репозиторий №{i}: {el.get("name")}')
