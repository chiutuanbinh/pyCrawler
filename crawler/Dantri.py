import hashlib
import json
import re
import time

import article_pb2
import scrapy
from xkafka import Producer

from crawler.Base import ArticleSpider
from crawler.common import invalid_links


class DantriSpider(ArticleSpider):
    name = 'dantri'
    start_urls = ['https://dantri.com.vn']
    allowed_domains = ['dantri.com.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%Y-%m-%dT%H:%M:%S'
    visited = set()
    def doParse(self, resp):
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
                            # self.logger.info(jata['datePublished'])

                            structTime = time.strptime(jata['datePublished'].split('.')[0], self.dtFormat)
                            ts = int(time.mktime(structTime) * 1000)
                            pArticle.timestamp = ts
                pArticle.oriUrl = resp.request.url
                pArticle.title = resp.css('title::text').get().replace('| Báo Dân trí','')
                pArticle.id = hashlib.md5(resp.request.url.encode()).hexdigest()
                pArticle.publisher = self.name
                media_list = []
                for img in article_body.css('img'):
                    media_url = img.css('img::attr(src)').get()
                    if media_url is not None:
                        media_list.append(media_url)
                pArticle.mediaUrl.extend(media_list)
                return pArticle
        return None
