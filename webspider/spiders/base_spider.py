import scrapy

class BaseSpider(scrapy.Spider):
    name = 'base'

    def start_requests(self):
        raise NotImplemented

    def parse(self, response):
        raise NotImplemented

