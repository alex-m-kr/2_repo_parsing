'''
Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы получаем должность) с сайтов
HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать
несколько страниц сайта (также вводим через input или аргументы). Получившийся
список должен содержать в себе минимум:
1. Наименование вакансии.
2. Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта.
цифры преобразуем к цифрам).
3. Ссылку на саму вакансию.
4. Сайт, откуда собрана вакансия.
'''

# Не совсем понял п.4 - Сайт, откуда собрана вакансия.
# Поэтому в список включать много раз один и тот же сайт (hh.ru) не стал.

import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import salary

# https://belgorod.hh.ru/search/vacancy?clusters=true&area=113&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=PYTHON&page=0
url = 'https://belgorod.hh.ru/search/vacancy?clusters=true&area=113&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy'
name = 'PYTHON'
params = {'text': name, "page": 0}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
vacancys = []
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
        # print(vacancy_name)
        # print(vacancy_link)
        # print(vacancy_salary_line)
        # if vacancy_salary_line is not None:
        #     for c in vacancy_salary_line:
        #         print(ord(c), end=' ')
        # print(salary.salary_parser(vacancy_salary_line))

        vacancy_data['page'] = params['page'] + 1
        vacancy_data['№'] = cnt
        vacancy_data['name'] = vacancy_name
        vacancy_data['salary'] = salary.salary_parser(vacancy_salary_line)
        vacancy_data['link'] = vacancy_link
        vacancys.append(vacancy_data)
        cnt += 1
    params['page'] += 1

with open('hw2.json', 'w', encoding='utf-8') as f:
    json.dump(vacancys, f, ensure_ascii=False, indent=2)

pprint(vacancys)
