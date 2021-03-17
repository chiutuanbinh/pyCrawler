import scrapy
import re
import article_pb2
from xkafka import Producer
import hashlib
import time
import json


class TuoitreSpider(scrapy.Spider):
    name = 'tuoitre'
    start_urls = ['https://tuoitre.vn/cuu-chu-tich-ha-noi-nguyen-duc-chung-bi-khoi-to-them-toi-danh-vu-che-pham-redoxy-3c-20210317195908077.htm']
    allowed_domains = ['tuoitre.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%Y-%m-%dT%H:%M:%S%Z:00'
    visited = set()
    def parse(self, resp):
        if len(resp.css('div#main-detail-body').getall()) > 0 :
            article_body = resp.css('div#main-detail-body')
            datas = article_body.css('p::text').getall()
            
            if len(datas) > 0:
                datas = [d.replace('\xa0', ' ').strip() for d in datas]
                self.logger.info(datas)
                pArticle = article_pb2.PArticle()
                pArticle.paragraph.extend(datas)
                for meta in resp.css('meta'):
                    if meta.css('meta::attr(name)').get() == 'description':
                        desc = meta.css('meta::attr(content)').get().strip()
                        pArticle.description = desc
                    elif meta.css('meta::attr(name)').get() == 'keywords':
                        keywords = meta.css('meta::attr(content)').get().split(',')
                        pArticle.oriKeywords.extend(pArticle.oriKeywords.extend(keywords))
                    elif meta.css('meta::attr(property)').get() == 'article:published_time':
                        structTime = time.strptime(meta.css('meta::attr(content)').get(), self.dtFormat)
                        pArticle.timestamp = int(time.mktime(structTime) * 1000)
                pArticle.oriUrl = resp.request.url
                pArticle.title = resp.css('title::text').get().replace(' - Tuổi Trẻ Online','')
                pArticle.id = hashlib.md5(resp.request.url.encode()).hexdigest()
                
                self.logger.info(pArticle)
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
        #             self.logger.info(href)
        #             yield resp.follow(href, self.parse)
