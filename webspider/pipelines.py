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
    file = None

    def open_spider(self, spider):
        self.file = open('{0}/items.jl'.format(self.file_path), 'w')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


