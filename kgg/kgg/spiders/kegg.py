# _*_ coding: utf-8 _*_
import scrapy
from urllib import request
import re


class KeggSpider(scrapy.Spider):
    name = "kegg"
    page = request.urlopen('http://rest.kegg.jp/list/disease')
    html = page.read()
    html = html.decode('utf-8')
    ds = re.findall(r'ds:(.*?)\s\S', html)
    # lists = []
    # for l in ds:
    #     lists.append('http://www.genome.jp/dbget-bin/www_bget?ds:' + l)
    # print(lists)
    # start_urls = [
    #     'http://www.genome.jp/dbget-bin/www_bget?ds:' + l for l in ds
    # ]
    start_urls = [
        'http://www.genome.jp/dbget-bin/www_bget?ds:H00001'
    ]

    def parse(self, response):
        # url = response.url
        trs = response.xpath("//td[@class='fr5']/table/tr/th/nobr/text()\
        ").extract()
        tds = response.xpath(".//td[@class='fr5']/table/tr/td").extract()
        for tr in range(0, len(trs)):
            name = trs[tr]
            vals = tds[tr]
            print("name:", name)
            print("value:", vals)
            print("*" * 30)
