import scrapy
import Producer

class PnjSpider(scrapy.Spider):
    name = 'pnj'
    start_urls = ['https://giavang.pnj.com.vn/']
    allowed_domains=['giavang.pnj.com.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    def parse(self, resp):
        rows = resp.css('table>tbody>tr')
        pnjRow = rows[1].css('td::text').getall()
        scjRow = rows[2].css('td::text').getall()
        Producer.notify("pnj", b'price', bytes(pnjRow[1], encoding="raw_unicode_escape"))

        
        
        pass
        