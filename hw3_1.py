'''
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию.
Добавить в решение со сбором вакансий(продуктов) функцию, которая будет добавлять только новые
вакансии/продукты в вашу базу.
'''

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import salary

client = MongoClient('localhost', 27017)
db = client['gb_vacancy']
collection = db.hh

# https://belgorod.hh.ru/search/vacancy?clusters=true&area=113&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=PYTHON&page=0
url = 'https://belgorod.hh.ru/search/vacancy?clusters=true&area=113&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy'
name = 'PYTHON'
site = 'hh.ru'
params = {'text': name, "page": 0}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
# vacancys = []
cnt = 1

while True:

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    vacancys_list = soup.find_all('div', attrs={
        'class': 'vacancy-serp-item'})
    # print(len(vacancys_list))

    if not vacancys_list or not response.ok:
        break

    for vacancy in vacancys_list:
        vacancy_data = {}
        vacancy_info = vacancy.find('a', attrs={'class': 'bloko-link'})
        vacancy_name = vacancy_info.text
        vacancy_link = vacancy_info['href']
        try:
            vacancy_salary_line = vacancy.find('span', attrs={
                'data-qa': 'vacancy-serp__vacancy-compensation'}).text
        except:
            vacancy_salary_line = None

        vacancy_data['_id'] = cnt
        vacancy_data['page'] = params['page'] + 1
        vacancy_data['№'] = cnt
        vacancy_data['name'] = vacancy_name
        vacancy_data['salary'] = salary.salary_parser(vacancy_salary_line)
        vacancy_data['link'] = vacancy_link
        vacancy_data['site'] = site
        # vacancys.append(vacancy_data)

        try:
            collection.insert_one(vacancy_data)
        except dke:
            print('Документ уже существует, выходим из программы')
            exit()

        cnt += 1
    params['page'] += 1
