from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram.spiders.instaspawn import InstaspawnSpider
from instagram import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    users = input('Введите имена пользователей через  пробел: ').split()

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaspawnSpider, users_for_parse=users)

    process.start()
