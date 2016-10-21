# _*_ coding: utf-8 _*_
'''采集新浪新闻(国内新闻)'''
import scrapy
import re
from news.items import NewsItem


class SinaNews(scrapy.Spider):
    name = "sina"
    allowed_domains = ['news.sina.com.cn']
    start_urls = [
        'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_1.shtml'
    ]

    def parse(self, response):
        for site in response.xpath("//ul[@class='list_009']/li"):
            url = str(site.xpath("a/@href").extract()[0])
            # print("url:", url)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        # print("title", response.xpath(
        #     '//h1[@id="artibodyTitle"]/text()').extract())
        item = NewsItem()
        title = response.xpath('//h1[@id="artibodyTitle"]/text()').extract()[0]
        if title:
            item['title'] = title
        else:
            title['title'] = ""
        time = response.xpath(
            '//span[@id="navtimeSource"]/text()').extract()[0]
        if title:
            item['time'] = time
        else:
            item['time'] = ""
        source = response.xpath(
            '//span[@data-sudaclick="media_name"]/a/text()').extract()[0]
        if source:
            item['source'] = source
        else:
            item['source'] = ""
        desc = response.xpath('//div[@id="artibody"]').extract()[0]
        if desc:
            desc1 = re.findall(
                r'<div.*?>([\s\S]*)</div>', str(desc))[0]
            reg = re.findall(r'(<p class="article-editor">[\s\S]*</p>)',
                             str(desc1))
            desc = desc1.replace(reg[0], '')
        if desc:
            item['desc'] = desc.replace("'", '"')
        else:
            item['desc'] = ""
        editor = response.xpath(
            '//p[@class="article-editor"]/text()').extract()[0]
        if editor:
            item['editor'] = editor
        else:
            item['editor'] = ""
        item['link'] = str(response.url)
        print("link:", response.url)
        return item
