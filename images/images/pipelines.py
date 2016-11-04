# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from images.items import ImagesItem


class ImagesPipeline(object):
    def process_item(self, item, spider):
        print("image_urls", ImagesItem.image_urls)
        print("images", ImagesItem.images)
        return item
