# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def clear_price(value):
    try:
        value = float(value.replace(' ', ''))
    except:
        return value
    return value

# Здесь обработка тоже не получилась, прилеает строка, xpath применить не получается
# def process_spec(spec):
#     spec_dic = {}
#     for el in spec:
#         k = el.xpath('./dt/text()').get()
#         v = el.xpath('./dd/text()').get()
#         v = v.strip()
#         spec_dic[k] = v
#     return spec_dic


class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    # spec = scrapy.Field(input_processor=MapCompose(process_spec), output_processor=TakeFirst())
    spec = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field()
    _id = scrapy.Field()
