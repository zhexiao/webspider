# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os


class WebspiderPipeline(object):
    """
    保存数据
    """
    file_path = '{0}/results'.format(os.getcwd())
    tpl_path = '{0}/tpl'.format(os.getcwd())
    data = []

    def open_spider(self, spider):
        """
        called when the spider is opened.
        :param spider:
        :return:
        """
        self.data = []

    def process_item(self, item, spider):
        """
        called for every item pipeline component
        :param item:
        :param spider:
        :return:
        """
        dict_item = dict(item)
        if len(dict_item) > 0:
            self.data.append(dict_item)

        return item

    def close_spider(self, spider):
        """
        called when the spider is closed.
        :param spider:
        :return:
        """
        self.generate_html(spider, self.data)

    @classmethod
    def generate_json(cls, data):
        """
        生成json文件
        :param data:
        :return:
        """
        with open('{0}/items.jl'.format(cls.file_path), 'w') as _file:
            _file.write(json.dumps(data))

    @classmethod
    def generate_html(cls, spider, data):
        """
        生成html
        :param spider:
        :param data:
        :return:
        """

        # 生成a数据
        body_content = ""
        a_content = "<div><a href='{0}' target='_blank'>{1}</a></div>"
        for i, dt in enumerate(data):
            body_content += a_content.format(
                dt['link'],
                '{0}. {1}'.format(i, dt['text'])
            )

        # 读取模板文件字符串
        with open('{0}/res_tpl.html'.format(cls.tpl_path), 'r') as _file:
            html_content = _file.read()

        # 生成文件的html文件名
        filename = "{0}_{1}_{2}.html".format(
            spider.keyword,
            spider.start_page,
            spider.end_page
        )
        # 将a的内容写入到html里面
        with open('{0}/{1}'.format(cls.file_path, filename), 'w') as _file:
            _file.write(html_content.replace('{body_content}', body_content))
