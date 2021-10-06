'''
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше
введённой суммы (необходимо анализировать оба поля зарплаты - минимальнную и максимульную).
'''

from pymongo import MongoClient
from currency_rate import rub_to_usd_or_eur

limit_rub = 350000  # сумма в руб. можно было сделать через input()
limit_usd = rub_to_usd_or_eur(limit_rub, 'usd')
limit_eur = rub_to_usd_or_eur(limit_rub, 'eur')
print(f'Ищем з/п больше {limit_rub} руб., {limit_usd:.2f} usd, {limit_eur:.2f} eur.')

client = MongoClient('localhost', 27017)
db = client['gb_vacancy']
collection = db.hh

result1 = collection.find({
    'salary.currency': 'руб.',
    '$or': [ {'salary.from': {'$gt': limit_rub}}, {'salary.to': {'$gt': limit_rub}} ]
})
result2 = collection.find({
    'salary.currency': 'usd',
    '$or': [ {'salary.from': {'$gt': limit_usd}}, {'salary.to': {'$gt': limit_usd}} ]
})
result3 = collection.find({
    'salary.currency': 'eur',
    '$or': [ {'salary.from': {'$gt': limit_eur}}, {'salary.to': {'$gt': limit_eur}} ]
})

print('Результаты с з/п в руб.')
for doc in result1:
    print(doc)
print('Результаты с з/п в usd.')
for doc in result2:
    print(doc)
print('Результаты с з/п в eur.')
for doc in result3:
    print(doc)
'''
Ищем з/п больше 350000 руб., 4823.02 usd, 4158.14 eur.
Результаты с з/п в руб.
{'_id': 7, 'page': 1, '№': 7, 'name': 'Python разработчик', 'salary': {'currency': 'руб.', 'from': None, 'to': 380000}, 'link': 'https://belgorod.hh.ru/vacancy/47682360?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 22, 'page': 2, '№': 22, 'name': 'Python developer', 'salary': {'currency': 'руб.', 'from': None, 'to': 400000}, 'link': 'https://belgorod.hh.ru/vacancy/47322083?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 47, 'page': 3, '№': 47, 'name': 'Python developer', 'salary': {'currency': 'руб.', 'from': None, 'to': 400000}, 'link': 'https://belgorod.hh.ru/vacancy/47820200?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 54, 'page': 3, '№': 54, 'name': 'Back-end Developer (Solidity+Django)', 'salary': {'currency': 'руб.', 'from': 600000, 'to': None}, 'link': 'https://belgorod.hh.ru/vacancy/48243893?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 533, 'page': 27, '№': 533, 'name': 'Senior Data Scientist в команду генетики', 'salary': {'currency': 'руб.', 'from': None, 'to': 450000}, 'link': 'https://belgorod.hh.ru/vacancy/47866453?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 550, 'page': 28, '№': 550, 'name': 'Ведущий разработчик (Full stack, Team lead)', 'salary': {'currency': 'руб.', 'from': 400000, 'to': None}, 'link': 'https://belgorod.hh.ru/vacancy/47640922?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 612, 'page': 31, '№': 612, 'name': 'Программист-разработчик Frontend/Backend/Fullstack (Удаленно)', 'salary': {'currency': 'руб.', 'from': 150000, 'to': 400000}, 'link': 'https://belgorod.hh.ru/vacancy/48242303?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 647, 'page': 33, '№': 647, 'name': 'Back-end Developer', 'salary': {'currency': 'руб.', 'from': 300000, 'to': 390000}, 'link': 'https://belgorod.hh.ru/vacancy/46390381?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 649, 'page': 33, '№': 649, 'name': 'DevOps Engineer', 'salary': {'currency': 'руб.', 'from': 250000, 'to': 400000}, 'link': 'https://belgorod.hh.ru/vacancy/48401473?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 668, 'page': 34, '№': 668, 'name': 'Senior Quantitative Researcher', 'salary': {'currency': 'руб.', 'from': 420000, 'to': None}, 'link': 'https://belgorod.hh.ru/vacancy/44675842?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
Результаты с з/п в usd.
{'_id': 18, 'page': 1, '№': 18, 'name': 'Data Scientist', 'salary': {'currency': 'usd', 'from': 3000, 'to': 5000}, 'link': 'https://belgorod.hh.ru/vacancy/47888798?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 27, 'page': 2, '№': 27, 'name': 'Python developer', 'salary': {'currency': 'usd', 'from': 1500, 'to': 5000}, 'link': 'https://belgorod.hh.ru/vacancy/48497664?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 97, 'page': 5, '№': 97, 'name': 'Senior Python Developer', 'salary': {'currency': 'usd', 'from': 4000, 'to': 5000}, 'link': 'https://belgorod.hh.ru/vacancy/47973163?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 156, 'page': 8, '№': 156, 'name': 'Senior Python/Django developer', 'salary': {'currency': 'usd', 'from': 3000, 'to': 5000}, 'link': 'https://belgorod.hh.ru/vacancy/48582354?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 334, 'page': 17, '№': 334, 'name': 'Team Lead Python Engineer', 'salary': {'currency': 'usd', 'from': None, 'to': 8000}, 'link': 'https://belgorod.hh.ru/vacancy/48251626?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 388, 'page': 20, '№': 388, 'name': 'Senior data engineer (python)', 'salary': {'currency': 'usd', 'from': 4000, 'to': 6000}, 'link': 'https://belgorod.hh.ru/vacancy/47876485?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 547, 'page': 28, '№': 547, 'name': 'Machine Learning Engineer (Remote/ relocate to Riga)', 'salary': {'currency': 'usd', 'from': 6000, 'to': 8000}, 'link': 'https://belgorod.hh.ru/vacancy/48551599?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 630, 'page': 32, '№': 630, 'name': 'Senior Software Engineer, Database Engineering (Cube Core)', 'salary': {'currency': 'usd', 'from': 6000, 'to': None}, 'link': 'https://belgorod.hh.ru/vacancy/46377490?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 698, 'page': 35, '№': 698, 'name': 'Senior/Lead ML Engineer', 'salary': {'currency': 'usd', 'from': 5000, 'to': 7000}, 'link': 'https://belgorod.hh.ru/vacancy/47584135?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 703, 'page': 36, '№': 703, 'name': 'Middle DevOps Engineer (relocation to Canada)', 'salary': {'currency': 'usd', 'from': 6500, 'to': None}, 'link': 'https://belgorod.hh.ru/vacancy/48586828?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 725, 'page': 37, '№': 725, 'name': 'Senior Infrastructure/DevOps Engineer (Cube Cloud)', 'salary': {'currency': 'usd', 'from': 8000, 'to': None}, 'link': 'https://belgorod.hh.ru/vacancy/48541270?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
Результаты с з/п в eur.
{'_id': 215, 'page': 11, '№': 215, 'name': 'Middle/Middle+ Python developer (Django/удаленно с Эстонией)', 'salary': {'currency': 'eur', 'from': None, 'to': 4500}, 'link': 'https://belgorod.hh.ru/vacancy/47673289?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 287, 'page': 15, '№': 287, 'name': 'Senior Python-разработчик', 'salary': {'currency': 'eur', 'from': 2000, 'to': 4500}, 'link': 'https://belgorod.hh.ru/vacancy/46245732?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 291, 'page': 15, '№': 291, 'name': 'Senior Python-разработчик', 'salary': {'currency': 'eur', 'from': 2000, 'to': 4500}, 'link': 'https://belgorod.hh.ru/vacancy/46245822?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
{'_id': 503, 'page': 26, '№': 503, 'name': 'Middle/Middle+ Python developer (Django/удаленно с Эстонией)', 'salary': {'currency': 'eur', 'from': None, 'to': 4500}, 'link': 'https://belgorod.hh.ru/vacancy/47673289?from=vacancy_search_list&query=PYTHON', 'site': 'hh.ru'}
'''
