from crawler.Base import ArticleSpider
import hashlib
import html
import json
import re
import time

import article_pb2
import scrapy
from xkafka import Producer

from crawler.common import invalid_links


class VTVSpider(ArticleSpider):
    name = 'VTV'
    start_urls = ['https://vtv.vn/kinh-te/tu-ngay-1-7-tang-muc-chuan-tro-giup-xa-hoi-len-360000-dong-thang-20210317193546918.htm']
    allowed_domains = ['vtv.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%Y-%m-%dT%H:%M:%S%Z:00'
    visited = set()
    def doParse(self, resp):
        if len(resp.css('div#entry-body').getall()) > 0 :
            article_body = resp.css('div#entry-body')
            datas = article_body.css('p::text').getall()
            
            if len(datas) > 0:
                datas = [d.replace('\xa0', ' ').strip() for d in datas]
                # self.logger.info(datas)
                pArticle = article_pb2.PArticle()
                pArticle.paragraph.extend(datas)
                for meta in resp.css('meta'):
                    if meta.css('meta::attr(name)').get() == 'description':
                        desc = meta.css('meta::attr(content)').get().strip()
                        pArticle.description = html.unescape(desc)
                    elif meta.css('meta::attr(name)').get() == 'keywords':
                        keywords = meta.css('meta::attr(content)').get().split(',')
                        pArticle.oriKeywords.extend(pArticle.oriKeywords.extend(keywords))
                for jdata in resp.css('script'):
                    if jdata.css('script::attr(type)').get() == 'application/ld+json':
                        data = jdata.css('script::text').get().strip()
                        jata = json.loads(data)
                        if 'datePublished' in jata.keys():
                            structTime = time.strptime(jata['datePublished'], self.dtFormat)
                            ts = int(time.mktime(structTime) * 1000)
                            pArticle.timestamp = ts
                pArticle.title = resp.css('title::text').get().replace('| VTV.VN','').strip()
                pArticle.oriUrl = resp.request.url
                pArticle.publisher = self.name
                pArticle.id = hashlib.md5(resp.request.url.encode()).hexdigest()
                return pArticle
        return None