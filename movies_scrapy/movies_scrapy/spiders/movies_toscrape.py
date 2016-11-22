# -*- coding: utf-8 -*-
import scrapy


class MoviesToscrapeSpider(scrapy.Spider):
    name = "movies-toscrape"
    allowed_domains = ["baidu.com"]
    start_urls = [
        'https://1geauomti8yzdrct1fa4d1mmrgrzgramjct4zya5uf3ts65e.ourdvsss.com/d1.baidupcs.com/file/b1a4a99fd40c45c4063321ce670afc81?bkt=p3-000062e4dbd973a58e405b88298782140295&xcode=6a8fd793c2814ca31ac359699add2473804abbf5375f54b8ded0b7c77404c736&fid=2824442831-250528-942134883494784&time=1478757176&sign=FDTAXGERLBH-DCb740ccc5511e5e8fedcff06b081203-kFLXun%2BAlFSDb8Qydn4RbGLopms%3D&to=sf&fm=Yan,B,U,nc&sta_dx=80137091&sta_cs=86&sta_ft=mp4&sta_ct=1&sta_mt=1&fm2=Yangquan,B,U,nc&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=000062e4dbd973a58e405b88298782140295&sl=75956300&expires=8h&rt=sh&r=270658390&mlogid=7295962051492883445&vuk=2118497912&vbdid=2991109281&fin=%E5%AD%99%E5%AD%90%E6%B6%B5%20-%20%E6%9C%80%E7%BE%8E%E4%B8%8D%E8%BF%87%E5%88%9D%E7%9B%B8%E8%A7%81.mp4&fn=%E5%AD%99%E5%AD%90%E6%B6%B5%20-%20%E6%9C%80%E7%BE%8E%E4%B8%8D%E8%BF%87%E5%88%9D%E7%9B%B8%E8%A7%81.mp4&slt=pm&uta=0&rtype=1&iv=0&isw=0&dp-logid=7295962051492883445&dp-callid=0.1.1&hps=1&csl=600&csign=mNXxkAlpW8OTY9aLjIZX%2FqQTRVY%3D&wshc_tag=0&wsts_tag=58240b39&wsid_tag=8cce30aa&wsiphost=ipdbm',
        # 'http://pan.baidu.com/s/1sjnBptr',
        # 'http://pan.baidu.com/s/1sjxKBjZ',
        # 'http://pan.baidu.com/s/1dDkDYyH',
        # 'http://pan.baidu.com/s/1keipK'
    ]

    def parse(self, response):
        print("url:", response.url)
        print("header:", response.header)
