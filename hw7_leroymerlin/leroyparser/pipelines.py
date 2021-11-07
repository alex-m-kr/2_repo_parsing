# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroyparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.products

    def process_item(self, item, spider):
        # item['spec'] = self.process_spec(item['spec'])
        # print()
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

# такой способ не получился, здесь spec - это list и xpath не работает
    # def process_spec(self, spec):
    #     spec_dic = {}
    #     for el in spec:
    #         k = el.xpath('./dt/text()').get()
    #         v = el.xpath('./dd/text()').get()
    #         v = v.strip()
    #         spec_dic[k] = v
    #     return spec_dic

class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    img = img.replace('_82', '_600')  # меняем адрес картинки, чтобы получить нужный размер
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = request.url.split('/')[-1]
        part_url = item['link'].split('/')[-2]
        return f'{part_url}/{image_name}'
