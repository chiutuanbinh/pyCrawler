import scrapy
import re
import article_pb2
import hashlib
import time
from crawler.Base import ArticleSpider


class VnexpressSpider(ArticleSpider):
    name = 'vnexpress'
    start_urls = ['https://vnexpress.net/']
    allowed_domains = ['vnexpress.net']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%Y-%m-%dT%H:%M:%S%Z:00'

    def doParse(self, resp):
        if len(resp.css('article.fck_detail').getall()) > 0 :    
            
            article = resp.css('article.fck_detail')
            datas = article.css('p::text').getall()
            datas = [d.replace('\"', '').strip() for d in datas if d != '\n']
            if len(datas) != 0 :
                pArticle = article_pb2.PArticle()
                pArticle.paragraph.extend(datas)
                desc = resp.css('p.description::text').get()
                if desc is not None:
                    pArticle.description = desc
                for meta in resp.css('meta'):   
                    if meta.css('meta::attr(itemprop)').get() == 'articleSection':
                        # self.logger.info(meta.css('meta::attr(content)').get())
                        pArticle.oriCategory = meta.css('meta::attr(content)').get().strip()
                    elif meta.css('meta::attr(name)').get() == 'keywords':
                        pArticle.oriKeywords.extend([x.strip() for x in meta.css('meta::attr(content)').get().split(',')])
                        # self.logger.info(meta.css('meta::attr(content)').get())
                    elif meta.css('meta::attr(name)').get() == 'pubdate':
                        structTime = time.strptime(meta.css('meta::attr(content)').get(), self.dtFormat)
                        pArticle.timestamp = int(time.mktime(structTime) * 1000)
                    pass
                pArticle.oriUrl = resp.request.url
                pArticle.title = resp.css('title::text').get().replace('- VnExpress', '').strip()
                pArticle.publisher = self.name
                pArticle.id = hashlib.md5(resp.request.url.encode()).hexdigest()
                return pArticle
        return None
