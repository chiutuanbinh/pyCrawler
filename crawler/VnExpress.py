import scrapy
import re


class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    start_urls = ['https://vnexpress.net/']
    allowed_domains = ['vnexpress.net']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }

    def parse(self, resp):
        for article in resp.css('article.fck_detail'):
            datas = article.css('p::text').getall()
            if len(datas) == 0 :
                continue
            # self.logger.info({'content': datas})
        for meta in resp.css('meta'):
            # if meta.css('meta::attr(itemprop)').get() == 'articleSection':
            #     self.logger.info(meta.css('meta::attr(content)').get())
            if meta.css('meta::attr(name)').get() == 'keywords':
                self.logger.info(meta.css('meta::attr(content)').get())
        for next_page in resp.css('a'):
            if len(next_page.css('a::attr(href)').getall()) > 0:
                href = next_page.css('a::attr(href)').get()
                if href in ['javascript:;', 'javascript:void(0);', 'javascript:void(0)']:
                    pass
                elif re.search("(mailto|tel)", href) is not None:
                    pass
                else:
                    yield resp.follow(next_page, self.parse)
