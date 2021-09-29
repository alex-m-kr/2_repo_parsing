'''
2. Изучить список открытых API. Найти среди них любое, требующее авторизацию
(любого типа). Выполнить запросы к нему, пройдя авторизацию.
Ответ сервера записать в файл.
'''
import requests

token = 'e...'
my_user_id = '12270216'
url_user_get = 'https://api.vk.com/method/users.get'
text = []

my_params = {
    'user_id': my_user_id,
    'v': '5.131',
    'access_token': token
}

r = requests.get(url_user_get, params=my_params)
json_data = r.json()
text.append(f'{json_data}\n')
print(f'имя: {json_data.get("response")[0].get("first_name")}, '
      f'фамилия: {json_data.get("response")[0].get("last_name")}')
# имя: Алексей, фамилия: Крючков

print('Посмотрим пользователей с двумя первыми id')
for id in range(1, 3):
    my_params['user_id'] = str(id)
    r = requests.get(url_user_get, params=my_params)
    json_data = r.json()
    text.append(f'{json_data}\n')

    print(f'имя: {json_data.get("response")[0].get("first_name")}, '
          f'фамилия: {json_data.get("response")[0].get("last_name")}, '
          f'id: {json_data.get("response")[0].get("id")}')
# имя: Павел, фамилия: Дуров, id: 1
# имя: Александра, фамилия: Владимирова, id: 2

with open('hw1_2.txt', 'w', encoding='utf-8') as f:
    f.writelines(text)
