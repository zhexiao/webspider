import scrapy
from urllib.parse import urlparse
from collections import defaultdict


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
    next_page_signal = ('下一页', 'next')
    seen = defaultdict()

    def __init__(self,
                 url, keyword, start=1, end=3,
                 *args, **kwargs):
        super(LinksSpider, self).__init__(*args, **kwargs)

        # 参数
        self.url = url.rstrip('/')
        self.keyword = keyword
        self.start = start
        self.end = end

        self.validate_page_number()
        self.analysis_url()

    def start_requests(self):
        """
        请求数据
        :return:
        """
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        """
        解析数据
        :param response:
        :return:
        """
        for a_obj in response.css('a'):
            a_content = a_obj.xpath('text()').extract_first()

            if not a_content:
                continue
            a_content = a_content.strip().lower()

            found_url = a_obj.xpath('@href').extract_first()
            if not found_url:
                continue

            if found_url.startswith(
                    ('http', 'https')) and self.netloc not in found_url:
                continue

            prefix = None
            if not found_url.startswith(('http', 'https')):
                prefix = '{0}://'.format(self.scheme)

            if self.netloc not in found_url:
                prefix = '{0}{1}'.format(prefix, self.netloc)

            if prefix:
                found_url = '{0}/{1}'.format(prefix, found_url.lstrip('/'))

            if self.keyword.lower() in a_content:
                # 去重
                if self.seen.get(found_url):
                    continue
                self.seen[found_url] = True

                print(a_content, found_url)
                yield {
                    'text': a_content,
                    'link': found_url
                }

            if a_content in self.next_page_signal:
                yield response.follow(found_url, self.parse)

        # # 读取a里面的内容
        #     text = a_obj.xpath('text()').extract_first()
        #
        #     # 查看keyword是否在text里面
        #     if text and self.keyword in text.lower():
        #         not_found = False
        #         link = a_obj.xpath('@href').extract_first()
        #         link = '{0}/{1}'.format(self.http_domain, link)
        #
        #         # 去除相同URL的数据
        #         if link not in self.unique_url:
        #             self.unique_url.append(link)
        #         else:
        #             continue
        #
        #         print(text)
        #         yield {
        #             'text': text,
        #             'link': link
        #         }
        #
        # # 如果没有找到数据，返回空{}
        # if not_found:
        #     print('no data found!')
        yield {}

    def validate_page_number(self):
        """
        验证page number
        :return:
        """
        if not isinstance(self.start, (int,)):
            raise ValueError('start - 开始页需要为整数')

        if not isinstance(self.end, (int,)):
            raise ValueError('end - 结束页需要为整数')

        if self.end < self.start:
            raise ValueError('分页不合法，结束页大于开始页')

    def analysis_url(self):
        parse_res_obj = urlparse(self.url)
        self.netloc = getattr(parse_res_obj, 'netloc')
        self.scheme = getattr(parse_res_obj, 'scheme')
