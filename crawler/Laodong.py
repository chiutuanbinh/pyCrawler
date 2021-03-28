from crawler.Base import ArticleSpider
import scrapy
import re
import article_pb2
from xkafka import Producer
import hashlib
import time
import json
from crawler.common import invalid_links

class LaodongSpider(ArticleSpider):
    name = 'laodong'
    start_urls = ['https://laodong.vn']
    allowed_domains = ['laodong.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%Y-%m-%dT%H:%M:%S%Z:00'
    visited = set()
    def doParse(self, resp):
        if len(resp.css('div.article-content').getall()) > 0 :
            article_body = resp.css('div.article-content')
            datas = article_body.css('p::text').getall()
            
            if len(datas) > 0:
                datas = [d.replace('\xa0', ' ').strip() for d in datas]
                # self.logger.info(datas)
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
                pArticle.publisher = self.name
                imgs = article_body.css('img')
                media_list = []
                for img in imgs:
                    media_url = img.css('img::attr(src)').get()
                    if media_url is not None:
                        media_list.append(media_url)
                self.logger.info(media_list)
                pArticle.mediaUrl.extend(media_list)

                return pArticle
        return None