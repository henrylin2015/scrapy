# -*- coding: utf-8 -*-
"""
* @file:  kegg_dg.py
* @author: henry
* @time: Thu Nov  3 16:03:53 2016
* 抓取数据 http://www.kegg.jp/kegg/pathway.html#disease
"""
import scrapy
from sqlalchemy import create_engine


# MySQL log-in info
# ************change the login information when needed*******************
username = 'root'
password = ''
host_address = '127.0.0.1'
port = '3306'
database = 'test_ds'
# Connect to MySQL
connstr = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8\
'.format(username, password, host_address, port, database)
engine = create_engine(connstr)
# Connect to the database
conn = engine.connect()

# output table
# ****************** change the output table name when needed **************
output_pathway = 'kgg_pathway'
output_pathway_ids = 'kgg_pathway_ids'
output_table = 'kegg_dg'


class KeggDg(scrapy.Spider):
    name = "kegg_dg"
    allowed_domains = ["kegg.jp"]
    start_urls = [
        'http://www.kegg.jp/kegg/pathway.html#disease'
    ]

    def parse(self, response):
        pathway_index = response.xpath("//b[text()='6.2 Cancers: Specific types']\
        /following::table[1]//a/@href").extract()
        if pathway_index:
            for l in pathway_index:
                url = 'http://www.kegg.jp' + l
                # print("url:", url)
                yield scrapy.Request(url, callback=self.enter_parse)

    def enter_parse(self, response):
        tmp = response.xpath('//a[text()="Pathway entry"]/@href').extract()
        # print(tmp)
        url = 'http://www.kegg.jp' + tmp[0]
        # print("url:", url)
        url_souce = response.url
        yield scrapy.Request(url, meta={'pathwaymap': url_souce},
                             callback=self.handle)

    def handle(self, response):
        entry_url = response.url
        pathway_url = response.meta['pathwaymap']
        # print("entry url:", entry_url)
        # print("pathwaymap:", pathway_url)
        entry = ""
        try:
            entry_vale = response.xpath("//nobr[contains(./text(),'Entry')]\
            /parent::*[1]/following::td[1]//text()").extract()
            if entry_vale:
                try:
                    entry_vale.remove('\n')
                    entry_vale = ''.join(entry_vale)
                    entry = entry_vale.replace('\xa0', '').replace(
                        'Pathway', '')
                except Exception as e:
                    print("Error:", e)
                    print("Entry not fond", entry)
            else:
                print("Entry not fond")
        except Exception as e:
            print("Error:", e)
        print("tr:", entry)
        name = ""
        name_val = response.xpath('//nobr[contains(./text(),"Name")]/parent::*[1]\
/following::td[1]//text()').extract()
        if name_val:
            name = ''.join(name_val)

        description = ""
        description_val = response.xpath('//nobr[contains(./text(),"Description")]\
/parent::*[1]/following::td[1]//text()').extract()[0]
        if description_val:
            description = description_val

        clazz = ""
        clazz_val = response.xpath('//nobr[contains(./text(),"Class")]/parent::*[1]\
/following::td[1]//text()').extract()[0]
        if clazz_val:
            clazz = clazz_val

        # Disease的数据插入到数据库中
        disKeyList = []
        disValList = []
        disKey = response.xpath('//nobr[contains(./text(),"Disease")]/parent::*[1]\
/following::td[1]//a[contains(@href,"ds")]/text()').extract()
        if disKey:
            disKeyList = disKey
        disVal = response.xpath('//nobr[contains(./text(),"Disease")]/parent::*[1]\
/following::td[1]//div/text()').extract()
        if disVal:
            disValList = disVal
        # 插入数据中 Disease
        print("disKeyList:", disKeyList)
        if disKeyList and (len(disKeyList) == len(disValList)):
            for v in range(0, len(disKeyList)):
                self.saveDisease(entry, disKeyList[v], disValList[v],
                                 entry_url)
        # 插入数据中 Drug
        drugKey = response.xpath('//nobr[contains(./text(), "Drug")]/parent::*[1]\
/following::td[1]//a[contains(@href,"dr")]/text()').extract()
        drugVal = response.xpath('//nobr[contains(./text(), "Drug")]/parent::*[1]\
/following::td[1]//div/text()').extract()
        if (drugKey and drugVal) and (len(drugKey) == len(drugVal)):
            for i in range(0, len(drugKey)):
                self.saveDrug(entry, drugKey[i], drugVal[i], entry_url)
        # 插入数据中
        if conn.execute('INSERT INTO `{}` (`Entry`, `name`, `description`,\
 `class`, `page_url`, `pathwaymap_url`) VALUES(%s,%s,%s,%s,%s,%s)\
'.format(output_pathway), entry, name, description, clazz, entry_url,
                        pathway_url):
            print("insert ok! Entry:", entry)
        else:
            print("insert no! Entry:", entry)
            pass
#         Disease = ""
#         Disease_Code = ""
#         try:
#             diseaseList = response('//nobr[contains(./text(),"Disease")]\
# /parent::*[1]/following::td[1]//text()').extract()
#             # 判断是否有空格(\xa0\xa0)
#             if '\xa0\xa0' in diseaseList:
#                 diseaseList.remove('\xa0\xa0')
#             Disease = ''.join(diseaseList)
#         except Exception as e:
#                 print("Error:", e)

    def saveDisease(self, pathway_code, code, name, page_url):
        self.field_name = 'Disease'
        if conn.execute('INSERT INTO `{}` (`pathway_code`, `field_name`,\
        `code`, `name`,`page_url`) VALUES(%s,%s,%s,%s,%s)\
        '.format(output_pathway_ids), pathway_code, self.field_name, code,
                        name, page_url):
            print("insert into Ok! pathway_code:", pathway_code)
        else:
            print("insert into No! pathway_code:", pathway_code)
            pass

    # 添加到表kgg_pathway_ids
    def saveDrug(self, pathway_code, code, name, page_url):
        self.field_name = "Drug"
        if conn.execute('INSERT INTO `{}` (`pathway_code`, `field_name`,\
        `code`, `name`,`page_url`) VALUES(%s,%s,%s,%s,%s)\
        '.format(output_pathway_ids), pathway_code, self.field_name, code,
                        name, page_url):
            print("insert into Ok! pathway_code:", pathway_code)
        else:
            print("insert into No! pathway_code:", pathway_code)
            pass
