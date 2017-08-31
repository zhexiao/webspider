import scrapy
from urllib.parse import urlparse


class LinksSpider(scrapy.Spider):
    """
    运行方法：
    scrapy crawl links -L WARNING \
    -a url_tpl=http://bbs.cnhubei.com/forum-3-{page}.html \
    -a keyword=湖北 \
    -a start_page=1 \
    -a end_page=5
    """

    name = "links"
    urls = []

    def __init__(self,
                 url_tpl, keyword, start_page=1, end_page=3,
                 *args, **kwargs):
        super(LinksSpider, self).__init__(*args, **kwargs)
        # 参数
        self.keyword = keyword
        self.start_page = start_page
        self.end_page = end_page
        self.domain = '//{0}'.format(urlparse(url_tpl).netloc)

        # 函数
        self.validate_page_number()
        self.generate_urls(url_tpl)


    def start_requests(self):
        """
        请求数据
        :return:
        """
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        解析数据
        :param response:
        :return:
        """
        not_found = True
        for a_obj in response.css('a'):
            # 读取a里面的内容
            text = a_obj.xpath('text()').extract_first()

            # 查看keyword是否在text里面
            if text and self.keyword in text:
                not_found = False
                link = a_obj.xpath('@href').extract_first()
                link = '{}/{}'.format(self.domain, link)
                print(text, link)

                yield {
                    'text': text,
                    'link': link
                }

        # 如果没有找到数据，返回空{}
        if not_found:
            print('no data found!')
            yield {}

    def validate_page_number(self):
        """
        验证page number
        :return:
        """
        # 转为整形数据
        try:
            self.start_page = int(self.start_page)
            self.end_page = int(self.end_page)
        except:
            raise ValueError('page only accept number')

        if self.end_page < self.start_page:
            raise ValueError('end_page must bigger than start_page')

    def generate_urls(self, url_tpl):
        """
        通过url模板和page number生成url
        :param url_tpl:
        :return:
        """
        for pg in range(self.start_page, self.end_page):
            self.urls.append(url_tpl.format(page=pg))