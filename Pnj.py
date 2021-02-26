import scrapy
import re
from kafka import KafkaProducer

class PnjSpider(scrapy.Spider):
    name = 'pnj'
    start_urls = ['https://giavang.pnj.com.vn/']
    allowed_domains=['giavang.pnj.com.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    def parse(self, resp):
        for table in resp.css('table'):
            self.logger.info({'content': table.css('td::text').getall()})
        
        
        pass
        