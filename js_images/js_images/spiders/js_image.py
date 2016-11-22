# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time


class JsImageSpider(scrapy.Spider):
    name = "js-image"
    allowed_domains = ["douban.com"]
    start_urls = [
        'https://movie.douban.com/',
    ]

    def parse(self, response):
        print("ddddd:", response.xpath("//title/text()"))
        driver = webdriver.PhantomJS(executable_path='/Users/xiaolin/Documents\
/scrapy/js_images/plugin/phantomjs-2.1.1-macosx/bin/phantomjs')
        print("url:", response.url)
        driver.get(response.url)
        time.sleep(5)
        print("info:", driver.find_element_by_id('imgid').text)
        driver.close()
