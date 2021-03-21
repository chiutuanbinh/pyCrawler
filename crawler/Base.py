from inspect import Traceback, trace
import re

import scrapy
import traceback
from xkafka import Producer
from crawler.common import invalid_links


class ArticleSpider(scrapy.Spider):
    visited = set()
    name = 'unknown'
    def doParse(self, resp):
        return None
    def parse(self, resp):
        try:
            pArticle = self.doParse(resp)
            if pArticle != None :
                # self.logger.info("ec")
                Producer.notify('article', self.name.encode(), pArticle.SerializeToString())
                pass
        except Exception as e:
            print(traceback.format_exc())
            pass
        
        for next_page in resp.css('a'):
            if len(next_page.css('a::attr(href)').getall()) > 0:
                href = next_page.css('a::attr(href)').get()
                if href in invalid_links or 'javascript' in href or 'void' in href:
                    pass
                elif re.search("(mailto|tel)", href) is not None:
                    pass
                else:
                    if href in self.visited:
                        continue
                    self.visited.add(href)
                    yield resp.follow(href, self.parse)
        
