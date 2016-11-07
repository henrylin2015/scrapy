# -*- coding: utf-8 -*-
import scrapy
from images.items import ImagesItem


class ImageSpider(scrapy.Spider):
    name = "images"
    img_urls = [
        'http://www.microfotos.com/images/testimg/1-1.jpg',
        'http://www.microfotos.com/images/testimg/2-1turn.jpg',
        'http://www.microfotos.com/images/testimg/2-2turn.jpg',
        'http://www.microfotos.com/images/testimg/4-2.jpg',
        'http://www.microfotos.com/images/testimg/4-3.jpg'
    ]
    start_urls = [
        'http://www.microfotos.com/'
    ]

    def parse(self, response):
        imgs_url = response.xpath('//img[contains(@src,"/images")]\
/@src').extract()
        for v in imgs_url:
            item = ImagesItem()
            imgs = "http://www.microfotos.com" + v
            item['image_urls'] = imgs
            item['url'] = response.url
            yield item
