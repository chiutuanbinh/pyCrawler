from crawler.VTC import VTCSpider
from crawler.VTV import VTVSpider
from crawler.Laodong import LaodongSpider
from crawler.Tuoitre import TuoitreSpider
from crawler.Nhandan import NhandanSpider
from crawler.Dantri import DantriSpider
from scrapy.crawler import CrawlerProcess
from crawler.VnExpress import VnexpressSpider
from crawler.ThanhNien import ThanhNienSpider
from crawler.Vietnamnet import VietnamnetSpider
from crawler.Pnj import PnjSpider
if __name__ == '__main__':
    process = CrawlerProcess(
        {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    # process.crawl(VnexpressSpider)
    # process.crawl(ThanhNienSpider)
    # process.crawl(VietnamnetSpider)
    # process.crawl(DantriSpider)
    # process.crawl(NhandanSpider)
    # process.crawl(TuoitreSpider)
    # process.crawl(LaodongSpider)
    # process.crawl(VTVSpider)
    process.crawl(VTCSpider)
    # process.crawl(PnjSpider)
    process.start()
    
    pass
