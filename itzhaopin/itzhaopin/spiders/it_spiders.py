# -*- coding: utf-8 -*-
import scrapy
from itzhaopin.items import ItzhaopinItem


class ItSpiders(scrapy.Spider):
    name = "IT"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/"
    ]

    def parse(self, response):
        items = []
        for sel in response.xpath("//div[@id='site-list-content']"):
            item = ItzhaopinItem()
            # print("info:", sel)
            # print("div:",sel.xpath("//div[@class='site-title']/text()").extract())
            item['title'] = sel.xpath(
                "//div[@class='site-title']/text()").extract()
            item['desc'] = sel.xpath(
                "//div[@class='site-descr ']/text()").extract()
            items.append(item)
            return items
