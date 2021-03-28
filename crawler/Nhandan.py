from crawler.Base import ArticleSpider
import scrapy
import re
import article_pb2
from xkafka import Producer
import hashlib
import time
import json
from crawler.common import invalid_links


class NhandanSpider(ArticleSpider):
    name = 'nhandan'
    start_urls = ['https://nhandan.com.vn']
    allowed_domains = ['nhandan.com.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%m/%d/%Y %H:%M:%S'
    visited = set()
    def doParse(self, resp):
        if len(resp.css('div.box-content-detail').getall()) > 0 :
            article_body = resp.css('div.box-content-detail')
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
                pArticle.publisher = self.name
                imgs = article_body.css('img')
                media_list = []
                for img in imgs:
                    media_url = img.css('img::attr(src)').get()
                    if media_url is not None:
                        if 'nhandan.com.vn' not in media_url:
                            media_url = 'https://nhandan.com.vn/' + media_url
                        media_list.append(media_url)
                # self.logger.info(pArticle)
                pArticle.mediaUrl.extend(media_list)
                return pArticle
        return None