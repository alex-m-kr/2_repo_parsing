'''
1) Создать пауков по сбору данных о книгах с сайтов labirint.ru ...
Каждый паук должен собирать:
* Ссылку на книгу
* Наименование книги
* Автор(ы)
* Основную цену
* Цену со скидкой
* Рейтинг книги
3) Собранная информация должна складываться в базу данных
p.s. Работает, но не ясно почему в БД попадает только 63 документа,
а по двум точкам входа суммарно их должно быть 144 + 79 = 223
p.p.s. Вроде разобрался: послле того как стал помимо ValueError отлавливать также ошибку TypeError, которую
давала попытка привести к float None (некоторые книги не имеют цены)
вакансий в БД стало значительно больше.
'''
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintRuSpider(scrapy.Spider):
    name = 'labirint_ru'
    allowed_domains = ['labirint.ru']
    start_urls = [
        'https://www.labirint.ru/search/Linux/?stype=0',
        'https://www.labirint.ru/search/%D1%80%D0%B0%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%BF%D1%80%D0%B5%D1%81%D1%82%D1%83%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9/?stype=0&page=1'
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@title='Следующая']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='cover']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").get()
        authors = response.xpath("//a[@data-event-label='author']/text()").getall()
        basic_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        discounted_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()
        item = BookparserItem(link=link, name=name, authors=authors, basic_price=basic_price,
                              discounted_price=discounted_price, rating=rating)
        yield item
