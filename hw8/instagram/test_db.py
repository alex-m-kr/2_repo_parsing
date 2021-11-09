from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.instagram

request = input('Введите имя пользователя и тип запроса [followed, follows]: ').split()
type_of_request = True if request[1].lower() == 'followed' else False
collection = db[request[0]]

for idx, elem in enumerate(collection.find({'follow_flag': type_of_request}), 1):
    print(f'{idx})', elem.get('username'))
