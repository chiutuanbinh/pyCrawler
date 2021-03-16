import scrapy
import re
import article_pb2
from xkafka import Producer
import hashlib
import time
import json


class VietnamnetSpider(scrapy.Spider):
    name = 'vietnamnet'
    start_urls = ['https://vietnamnet.vn/vn/thoi-su/chinh-tri/thu-tuong-to-cong-tac-khong-phai-cap-tren-cua-bo-nganh-dia-phuong-720017.html']
    allowed_domains = ['vietnamnet.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat='%Y-%m-%dT%H:%M:%S%Z:00'
    visited = set()
    def parse(self, resp):
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
            

            self.logger.info(pArticle)
            Producer.notify('article', self.name.encode(), pArticle.SerializeToString())


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
