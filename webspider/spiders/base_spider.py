import scrapy


class BaseSpider(scrapy.Spider):
    def start_requests(self):
        raise NotImplemented

    def parse(self, response):
        raise NotImplemented
