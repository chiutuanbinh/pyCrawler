import scrapy
from xkafka import Producer
import time
import goldprice_pb2

class SjcSpier(scrapy.Spider):
    name = 'sjc'
    start_urls = ['https://sjc.com.vn/giavang/']
    allowed_domains=['sjc.com.vn']
    custom_settings = {
        'LOG_LEVEL' : 'INFO'
    }

    def parse():
        pass
    pass