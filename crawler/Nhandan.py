import scrapy
import re
import article_pb2
from xkafka import Producer
import hashlib
import time
import json


class NhandanSpider(scrapy.Spider):
    name = 'nhandan'
    start_urls = ['https://nhandan.com.vn/tin-tuc-su-kien/hoi-nghi-tong-ket-5-nam-hoat-dong-to-cong-tac-cua-thu-tuong-chinh-phu-638649/']
    allowed_domains = ['nhandan.com.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%m/%d/%Y %H:%M:%S'
    visited = set()
    def parse(self, resp):
        if len(resp.css('div.detail-content-body ').getall()) > 0 :
            article_body = resp.css('div.detail-content-body ')
            datas = article_body.css('p::text').getall()
            
            if len(datas) > 0:
                datas = [d.replace('\xa0', ' ').strip() for d in datas]
                pArticle = article_pb2.PArticle()
                pArticle.paragraph.extend(datas)
                for meta in resp.css('meta'):
                    if meta.css('meta::attr(name)').get() == 'description':
                        desc = meta.css('meta::attr(content)').get().replace('(Dân trí) -', '').strip()
                        pArticle.description = desc
                for jdata in resp.css('script'):
                    if jdata.css('script::attr(type)').get() == 'application/ld+json':
                        data = jdata.css('script::text').get().strip()
                        jata = json.loads(data)
                        if 'datePublished' in jata.keys():
                            structTime = time.strptime(jata['datePublished'][:-3], self.dtFormat)
                            ts = int(time.mktime(structTime) * 1000)
                            pArticle.timestamp = ts
                pArticle.oriUrl = resp.request.url
                pArticle.title = resp.css('title::text').get().replace('| Báo Dân trí','')
                pArticle.id = hashlib.md5(resp.request.url.encode()).hexdigest()
                
                self.logger.info(pArticle)
        for next_page in resp.css('a'):
            if len(next_page.css('a::attr(href)').getall()) > 0:
                href = next_page.css('a::attr(href)').get()
                if href in ['javascript:;','javascript:void();', 'javascript:void(0);', 'javascript:void(0)']:
                    pass
                elif re.search("(mailto|tel)", href) is not None:
                    pass
                else:
                    if href in self.visited:
                        continue
                    self.visited.add(href)
                    self.logger.info(href)
                    yield resp.follow(href, self.parse)