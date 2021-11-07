from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from sys import argv

from leroyparser import settings
from leroyparser.spiders.leroymerlinru import LeroymerlinruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    # Сделал для удобства отладки значение по умолчанию, если не введены параметры при запуске файла
    # Также пока не разобрался, почему при запуске из терминала runner.py
    # появляется ошибка
    # from leroyparser import settings
    # ModuleNotFoundError: No module named 'leroyparser'
    # пробовал запускать и с полными и относительными путями к интерпритатору и файлу.
    query = ' '.join(argv[1:])
    if not query:
        query = 'товары для уборки снега'
    process.crawl(LeroymerlinruSpider, query)
    process.start()
