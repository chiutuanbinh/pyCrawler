import scrapy
import re
from scrapy.crawler import CrawlerProcess
from crawler.VnExpress import VnexpressSpider
from crawler.Pnj import PnjSpider
if __name__ == '__main__':
    process = CrawlerProcess(
        {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    # process.crawl(VnexpressSpider)
    process.crawl(PnjSpider)
    process.start()
    
    pass
