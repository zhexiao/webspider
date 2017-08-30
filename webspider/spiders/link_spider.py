import scrapy
from urllib.parse import urlparse


class LinksSpider(scrapy.Spider):
    """
    运行方法：
    scrapy crawl links -L WARNING \
    -a url_tpl=http://bbs.cnhubei.com/forum-3-{page}.html \
    -a keyword=湖北
    """
    name = "links"
    urls = []
    pages = 20

    def __init__(self, url_tpl, keyword, page_number=None, *args, **kwargs):
        super(LinksSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.domain = '//{0}'.format(urlparse(url_tpl).netloc)

        self.validate_page_number(page_number)
        self.generate_urls(url_tpl)


    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        not_found = True
        for a_obj in response.css('a'):
            text = a_obj.xpath('text()').extract_first()

            if text and self.keyword in text:
                not_found = False
                link = a_obj.xpath('@href').extract_first()
                link = '{}/{}'.format(self.domain, link)
                print('find', text, link)

                yield {
                    'text': text,
                    'link': link
                }

        if not_found:
            print('no data found!')
            yield {}

    def validate_page_number(self, page_number):
        """
        验证page number
        :param page_number:
        :return:
        """
        try:
            page_number = int(page_number)
            if page_number > 0:
                self.pages = page_number
        except:
            pass

    def generate_urls(self, url_tpl):
        """
        通过url模板和page number生成url
        :param url_tpl:
        :return:
        """
        for i in range(1, self.pages):
            self.urls.append(url_tpl.format(page=i))