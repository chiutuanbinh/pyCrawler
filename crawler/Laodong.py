import scrapy
import re
import article_pb2
from xkafka import Producer
import hashlib
import time
import json


class LaodongSpider(scrapy.Spider):
    name = 'laodong'
    start_urls = ['https://laodong.vn/phap-luat/nguyen-chu-tich-ha-noi-nguyen-duc-chung-tiep-tuc-bi-khoi-to-890203.ldo']
    allowed_domains = ['laodong.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%Y-%m-%dT%H:%M:%S%Z:00'
    visited = set()
    def parse(self, resp):
        if len(resp.css('div.article-content').getall()) > 0 :
            article_body = resp.css('div.article-content')
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
                        keywords = meta.css('meta::attr(content)').get().split(';')
                        pArticle.oriKeywords.extend(pArticle.oriKeywords.extend(keywords))
                    elif meta.css('meta::attr(property)').get() == 'og:title':
                        title = meta.css('meta::attr(content)').get()
                        pArticle.title = title
                for jdata in resp.css('script'):
                    if jdata.css('script::attr(type)').get() == 'application/ld+json':
                        data = jdata.css('script::text').get().strip()
                        jata = json.loads(data)
                        if 'datePublished' in jata.keys():
                            structTime = time.strptime(jata['datePublished'], self.dtFormat)
                            ts = int(time.mktime(structTime) * 1000)
                            pArticle.timestamp = ts
                pArticle.oriUrl = resp.request.url
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
