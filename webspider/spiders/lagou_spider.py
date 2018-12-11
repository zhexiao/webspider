"""
拉勾网爬虫
"""
import scrapy
from .base_spider import BaseSpider


class DemoSpider(BaseSpider):
    name = 'lagou'

    def start_requests(self):
        addr = 'https://www.lagou.com/jobs/list_{0}?px=default&city={1}'
        language = getattr(self, 'language', 'all')
        city = getattr(self, 'city', '全国')

        url = addr.format(
            language, city
        )
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'title': response.css('title::text').extract()
        }

        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
