import scrapy
import re
from scrapy.crawler import CrawlerProcess
from VnExpress import VnexpressSpider
from Pnj import PnjSpider
if __name__ == '__main__':
    process = CrawlerProcess(
        {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(PnjSpider)
    process.start()
    pass