"""
scrapy crawl demo --loglevel=WARNING -o quotes.json
"""
import scrapy
from .base_spider import BaseSpider


class DemoSpider(BaseSpider):
    name = 'demo'

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        div_data = response.xpath('//div[@class="quote"]')

        for d_d in div_data:
            title = d_d.xpath('.//span[@class="text"]/text()').extract_first()
            tags = d_d.xpath(
                './/div[@class="tags"]/a[@class="tag"]/text()').extract()
            about_url = d_d.xpath('.//span[2]/a/@href').extract_first()

            # 生成绝对URL地址
            about_url = response.urljoin(about_url)
            yield {
                'title': title,
                'tags': tags,
                'about': about_url
            }
        #
        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
