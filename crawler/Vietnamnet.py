from crawler.Base import ArticleSpider
import scrapy
import re
import article_pb2
from xkafka import Producer
import hashlib
import time
import json
from crawler.common import invalid_links

class VietnamnetSpider(ArticleSpider):
    name = 'vietnamnet'
    start_urls = ['https://vietnamnet.vn/']
    allowed_domains = ['vietnamnet.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%d-%m-%YT%H:%M:%S%Z:00'
    visited = set()
    def doParse(self, resp):
        if len(resp.css('div#ArticleContent').getall()) > 0:
            article = resp.css('div#ArticleContent')
            datas = article.css('p::text').getall()
            if len(datas) != 0:
                datas = [d.replace('\xa0', ' ').strip() for d in datas]
                pArticle = article_pb2.PArticle()
                pArticle.paragraph.extend(datas)
                for meta in resp.css('meta'):
                    if meta.css('meta::attr(name)').get() == 'description':
                        pArticle.description = meta.css('meta::attr(content)').get()
                    elif meta.css('meta::attr(name)').get() == 'news_keywords':
                        pArticle.oriKeywords.extend(pArticle.oriKeywords.extend([x.strip() for x in meta.css('meta::attr(content)').get().split(',')]))
                for jdata in resp.css('script'):
                    if jdata.css('script::attr(type)').get() == 'application/ld+json':
                        data = jdata.css('script::text').get().strip()
                        jata = json.loads(data)
                        if 'datePublished' in jata.keys():
                            structTime = time.strptime(jata['datePublished'], self.dtFormat)
                            ts = int(time.mktime(structTime) * 1000)
                            pArticle.timestamp = ts
                pArticle.oriUrl = resp.request.url
                pArticle.title = resp.css('title::text').get().replace('- VietNamNet', '').strip()
                pArticle.id = hashlib.md5(resp.request.url.encode()).hexdigest()
                pArticle.publisher = self.name
                imgs = article.css('img')
                media_list = []
                for img in imgs:
                    media_url = img.css('img::attr(src)').get()
                    if media_url is not None:
                        media_list.append(media_url)
                pArticle.mediaUrl.extend(media_list)
                return pArticle
        return None