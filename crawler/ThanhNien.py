import scrapy
import re
import article_pb2
from xkafka import Producer
import hashlib

class ThanhNienSpider(scrapy.Spider):
    name = 'thanhnien'
    start_urls = ['https://thanhnien.vn/thoi-su/dang-lam-viec-voi-co-quan-chuc-nang-youtuber-tho-nguyen-xin-dung-de-ve-nghi-ngoi-1354445.html']
    allowed_domains=['thanhnien.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }

    visited = set()
    def parse(self, resp):
        if len(resp.css('div#abody').getall()) > 0:
            article_body = resp.css('div#abody')
            datas = article_body.getall()
            # datas = [d.replace('\r','').replace('\n','').strip() for d in datas]
            # datas = [d for d in datas if d != '']
            self.logger.info(datas[0])
            pass
        # for next_page in resp.css('a'):
        #     if len(next_page.css('a::attr(href)').getall()) > 0:
        #         href = next_page.css('a::attr(href)').get()
        #         if href in ['javascript:;','javascript:void();', 'javascript:void(0);', 'javascript:void(0)']:
        #             pass
        #         elif re.search("(mailto|tel)", href) is not None:
        #             pass
        #         else:
        #             if href in self.visited:
        #                 continue
        #             self.visited.add(href)
        #             # self.logger.info(href)
        #             yield resp.follow(href, self.parse)
        pass
    pass