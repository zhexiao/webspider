"""
scrapy crawl search --loglevel=WARNING -a keyword="高铁" -a url="http://bbs.cnhubei.com/forum-3-1.html" -o quotes.json
"""
import scrapy
from .base_spider import BaseSpider


class SearchSpider(BaseSpider):
    name = 'search'

    def start_requests(self):
        self.keyword = getattr(self, 'keyword', None)
        self.url = getattr(self, 'url', None)

        # 验证数据
        if not all((self.keyword, self.url)):
            raise ValueError('缺少必要的参数`keyword`或`url`')

        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        data_list = response.xpath('//a')

        for dt in data_list:
            url = dt.xpath('.//@href').extract_first()
            url_text = dt.xpath('.//text()').extract_first()

            if not all((url, url_text)):
                continue

            if self.keyword not in url_text:
                continue

            absolute_url = response.urljoin(url)
            yield {
                'text': url_text,
                'url': absolute_url
            }

        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
