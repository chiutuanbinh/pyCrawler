import scrapy
import re
import article_pb2
from xkafka import Producer
import hashlib
import time
import json


class DantriSpider(scrapy.Spider):
    name = 'dantri'
    start_urls = ['https://dantri.com.vn/xa-hoi/2-nguoi-tu-nan-20-nguoi-bi-thuong-tai-hoa-giang-xuong-tren-duong-di-le-20210316151826194.htm']
    allowed_domains = ['dantri.com.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%Y-%m-%dT%H:%M:%S'
    visited = set()
    def parse(self, resp):
        if len(resp.css('div.dt-news__content').getall()) > 0 :
            article_body = resp.css('div.dt-news__content')
            datas = article_body.css('p::text').getall()
            if len(datas) > 0:
                datas = [d.strip() for d in datas]
                pArticle = article_pb2.PArticle()
                pArticle.paragraph.extend(datas)
                for meta in resp.css('meta'):
                    if meta.css('meta::attr(name)').get() == 'description':
                        desc = meta.css('meta::attr(content)').get().replace('(Dân trí) -', '').strip()
                        pArticle.description = desc
                    elif meta.css('meta::attr(name)').get() == 'keywords':
                        keywords = meta.css('meta::attr(content)').get().split(',')
                        pArticle.oriKeywords.extend(keywords)
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
