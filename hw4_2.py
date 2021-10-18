'''
Написать приложение, которое собирает основные новости с сайта на выбор 
news.mail.ru, lenta.ru, yandex-новости. 
Для парсинга использовать XPath. 
Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
Сложить собранные новости в БД
'''
# Вариант 2 с обновлением БД

from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['gb_news']
collection = db.archive
cnt_before = collection.count_documents({})


url = 'https://lenta.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
items = dom.xpath("//time[@class='g-time']/..")

list_news = []

for item in items:
    news = {}
    news['source'] = url
    news['name'] = item.xpath("./text()")[0].replace(chr(160), ' ')  # замена неразрывного пробела
    news['link'] = url + item.xpath("./@href")[0]
    news['time_s'] = item.xpath(".//@datetime")[0]
    list_news.append(news)
    collection.update_one({'name': news.get('name')}, {'$set': news}, upsert=True)

cnt_after = collection.count_documents({})
pprint(list_news)

result = collection.find({}, {'_id': 0, 'name': 1, 'link': 1})
print()
for el in result:
    print(el)
print()
print(f'В базе было {cnt_before} документов, стало {cnt_after} документов, добавлено {cnt_after - cnt_before} документов.')

