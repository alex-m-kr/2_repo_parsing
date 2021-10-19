import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://mo.superjob.ru/vacancy/search/?keywords=PYTHON',
        'https://www.superjob.ru/vacancy/search/?keywords=PYTHON&geo%5Br%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('////a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[contains(@class, "icMQ_ _6AfZ9")]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1/span/text()').get()
        salary = response.xpath('//span[@class="_1h3Zg _2Wp8I _2rfUm _2hCDz"]/text()').get()
        city = response.xpath('//div[@class="f-test-address _3AQrx"]/span/span/text()').get()
        link = response.url
        item = JobparserItem(name=name, salary=salary, city=city, link=link)
        yield item
