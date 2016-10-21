# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ItzhaopinPipeline(object):
    def process_item(self, item, spider):
        print("henry:", item['desc'])
        # return item

    def open_spider(self, spider):
        print("henry open spider")

    def close_spider(self, spider):
        print("henry close spider")
