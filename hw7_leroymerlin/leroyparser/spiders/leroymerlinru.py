import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://belgorod.leroymerlin.ru/search/?q={query}']


    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('photo', '//img[@slot="thumbs"]/@src')
        # loader.add_xpath('spec', '//div[@class="def-list__group"]')

        # вижу, что здесь не совсем подходящее место для обработки,
        # но ни в piplenes, ни items работать с xpath не получилось
        spec = response.xpath('//div[@class="def-list__group"]')
        spec_dic = {}
        for el in spec:
            k = el.xpath('./dt/text()').get()
            v = el.xpath('./dd/text()').get()
            v = v.strip()
            spec_dic[k] = v
        loader.add_value('spec', spec_dic)
        return loader.load_item()

        # link = response.url
        # name = response.xpath('//h1/text()').get()
        # price = response.xpath('//span[@slot="price"]/text()').get()
        # spec = response.xpath('//div[@class="def-list__group"]')
        # photo = response.xpath('//img[@slot="thumbs"]/@src').getall()
        # yield LeroyparserItem(link=link, name=name, price=price, spec=spec, photo=photo)
