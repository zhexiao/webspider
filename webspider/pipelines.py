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
        with open('{0}/items.jl'.format(self.file_path), 'w') as _file:
            _file.write(json.dumps(self.data))


