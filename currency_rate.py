import requests
from bs4 import BeautifulSoup

url = 'http://www.cbr.ru/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

usd_div = soup.find('div', attrs={'class': 'col-md-2 col-xs-9 _dollar'})
eur_div = soup.find('div', attrs={'class': 'col-md-2 col-xs-9 _euro'})
usd_str = usd_div.findNext('div').text
eur_str = eur_div.findNext('div').text
usd = float(usd_str.split()[0].replace(',', '.'))
eur = float(eur_str.split()[0].replace(',', '.'))


def rub_to_usd_or_eur(amount, currency):
    if 'usd' in currency.lower():
        return amount / usd
    if 'eur' in currency.lower():
        return amount / eur


if __name__ == '__main__':
    print('Проверка')
    print(usd, eur)
    print(rub_to_usd_or_eur(100000, 'Usd'))
    print(rub_to_usd_or_eur(100000, 'EUR'))
