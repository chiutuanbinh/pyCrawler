import scrapy
import re
import article_pb2
from xkafka import Producer
import hashlib
import time


class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    start_urls = ['https://vnexpress.net/']
    allowed_domains = ['vnexpress.net']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%Y-%m-%dT%H:%M:%S%Z:00'

    def parse(self, resp):
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
                # for img in resp.css('img'):
                #     if img.css('img::attr(itemprop)').get() == 'contentUrl':
                #         pArticle.mediaUrl.append(img.css('img::attr(data-src)').get())
                
                self.logger.info(pArticle)
                Producer.notify('article', self.name.encode(), pArticle.SerializeToString())
                pass

            
        for next_page in resp.css('a'):
            if len(next_page.css('a::attr(href)').getall()) > 0:
                href = next_page.css('a::attr(href)').get()
                if href in ['javascript:;', 'javascript:void(0);', 'javascript:void(0)']:
                    pass
                elif re.search("(mailto|tel)", href) is not None:
                    pass
                else:
                    yield resp.follow(next_page, self.parse)
