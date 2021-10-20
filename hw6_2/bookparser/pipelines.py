# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.gb_book

    def process_item(self, item, spider):
        item['name'] = self.process_name(item['name'])
        item['basic_price'] = self.process_str_to_numb(item['basic_price'])
        item['discounted_price'] = self.process_str_to_numb(item['discounted_price'])
        item['rating'] = self.process_str_to_numb(item['rating'])
        # авторов показалось удобнее оставить в виде списка и не обрабатывать
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_str_to_numb(self, line):
        try:
            return float(line)
        except (ValueError, TypeError):
            return None

    def process_name(self, name):
        return name.split(':')[1].strip()
