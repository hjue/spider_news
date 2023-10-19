import scrapy


class CntvSpider(scrapy.Spider):
    name = "cntv"
    allowed_domains = ["cntv.cn"]
    start_urls = ["https://cntv.cn"]

    def parse(self, response):
        pass
