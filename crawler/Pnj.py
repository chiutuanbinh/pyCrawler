import scrapy
from xkafka import Producer
import time
import goldprice_pb2



class PnjSpider(scrapy.Spider):
    name = 'pnj'
    start_urls = ['https://giavang.pnj.com.vn/']
    allowed_domains=['giavang.pnj.com.vn']
    custom_settings = {
        'LOG_LEVEL':'INFO'
    }
    dtFormat = ' %d/%m/%Y %H:%M:%S '
    def parse(self, resp):
        rows = resp.css('table>tbody>tr')
        
        for r in rows[1:3]:
            dat = r.css('td::text').getall()
            self.logger.info(dat)
            pPrice = goldprice_pb2.PGoldprice()
            pPrice.gType = dat[0]
            pPrice.buy = int(dat[1].replace('.',''))
            pPrice.sell = int(dat[2].replace('.',''))
            structTime = time.strptime(dat[3], self.dtFormat)
            pPrice.timestamp = int(time.mktime(structTime) * 1000)
            Producer.notify("gold", pPrice.gType.encode(), pPrice.SerializeToString())
        td = resp.css('#world-gold-price')
        print(td)
        buy = td.css('tr>td>strong>font').getall()[0]
        sell = td.css('tr>td>strong>font').getall()[1]
        self.logger.info(buy)
        self.logger.info(sell)

        # time.sleep(10)
        
        
        