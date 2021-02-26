import scrapy
import re
from scrapy.crawler import CrawlerProcess


class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    start_urls = ['https://vnexpress.net/']
    allowed_domains = ['vnexpress.net']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }

    def parse(self, resp):
        for article in resp.css('article.fck_detail'):
            self.logger.info({'content': article.css('p::text').getall()})
        for next_page in resp.css('a'):
            if len(next_page.css('a::attr(href)').getall()) > 0:
                href = next_page.css('a::attr(href)').get()
                if href in ['javascript:;', 'javascript:void(0);', 'javascript:void(0)']:
                    pass
                elif re.search("(mailto|tel)", href) is not None:
                    pass
                else:
                    yield resp.follow(next_page, self.parse)
