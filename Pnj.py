import scrapy
import Producer
import time
import goldprice_pb2



class PnjSpider(scrapy.Spider):
    name = 'pnj'
    start_urls = ['https://giavang.pnj.com.vn/']
    allowed_domains=['giavang.pnj.com.vn']
    custom_settings = {
        'LOG_LEVEL':'ERROR'
    }
    dtFormat = ' %d/%m/%Y %H:%M:%S '
    def parse(self, resp):
        rows = resp.css('table>tbody>tr')
        pnjRow = rows[1].css('td::text').getall()
        sjcRow = rows[2].css('td::text').getall()
        pnjPrice = goldprice_pb2.goldprice()
        pnjPrice.gType = pnjRow[0]
        pnjPrice.buy= int(pnjRow[1].replace('.', ''))
        pnjPrice.sell= int(pnjRow[2].replace('.', ''))
        structTime = time.strptime(pnjRow[3], self.dtFormat)
        pnjPrice.timestamp = int(time.mktime(structTime) * 1000)

        sjcPrice = goldprice_pb2.goldprice()
        sjcPrice.gType = sjcRow[0]
        sjcPrice.buy= int(sjcRow[1].replace('.', ''))
        sjcPrice.sell= int(sjcRow[2].replace('.', ''))
        structTime = time.strptime(sjcRow[3], self.dtFormat)
        sjcPrice.timestamp = int(time.mktime(structTime) * 1000)
        # print(pnjPrice)
        # print(pnjPrice.SerializeToString())
        Producer.notify("price", b'pnj', pnjPrice.SerializeToString())
        Producer.notify("price", b'sjc', sjcPrice.SerializeToString())
        
        
        
        pass
        