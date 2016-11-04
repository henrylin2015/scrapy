# -*- coding: utf-8 -*-
import scrapy
import re
from sqlalchemy import *
from sqlalchemy import create_engine
from urllib import request
import pandas as pd

'''
 @file:  pathway.py
 @author: henry
 @time: Thu Nov  3 11:22:41 2016
 @ 继承医药
'''

# MySQL log-in info
# ************change the login information when needed*******************
username = 'root'
password = ''
host_address = 'localhost'
port = '3306'
database = 'test_ds'

# Connect to MySQL
connstr_store = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8\
'.format(username, password, host_address, port, database)
engine_store = create_engine(connstr_store)
connection_store = engine_store.connect()  # Connect to the database

# output table
# **************change the output table name when needed*********************
output_table_keggpathway = 'kegg_pathway'
output_table_pathway_otherinfo = 'kegg_pathway_ids'

# Read existed data into a list
df = pd.read_sql('SELECT DISTINCT `pathway_code` FROM {} \
'.format(output_table_keggpathway), con=engine_store)
# the existed records
pathway_lst = df['pathway_code'].tolist()


class Pathway(scrapy.Spider):
    name = "pathway"
    allowed_domains = ["kegg.jp"]
    # get the pathway list
    page = request.urlopen('http://rest.kegg.jp/list/pathway/hsa')
    html = page.read()
    html = html.decode('utf-8')
    hsas = re.findall('path:(.*?)\t', html)
    page_map = request.urlopen('http://rest.kegg.jp/list/pathway')
    html_map = page_map.read()
    html_map = html_map.decode('utf-8')
    mp = re.findall('path:(.*?)\t', html_map)
    pw = hsas + mp
    start_urls = ["http://www.kegg.jp/dbget-bin/www_bget?pathway+" +
                  l for l in pw]

    def parse(self, response):
        print('nonono')
        entry_value = response.xpath("//nobr[contains(./text(),'Entry')]\
        /parent::*/parent::*/td//text()").extract()
        try:
            # Clear single '/n' the results still contains'/n',
            # e.g:Camostat mesilate [DR:D01766]/nNafamostat [DR:D01670]
            # which can be used in the later cleaning process
            entry_value.remove('\n')
            # convert list to string
            entry_value = ''.join(entry_value)
            entry_value = entry_value.replace('\xa0', '').replace('Pathway',
                                                                  '')
        except:
            print('error: no entry')
        if entry_value not in pathway_lst:
            if 'Drug'in entry_value:
                pass
            else:
                pathway_lst.append(entry_value)
                pathway_name =response.xpath("//nobr[contains(./text(),'Name')]/parent::*/parent::*/td//text()").extract()
                try:
                    pathway_name.remove('\n')
                except:
                    pass
                pathway_name = ''.join(pathway_name)

                description = response.xpath("//nobr[contains(./text(),'Description')]/parent::*/parent::*/td//text()").extract()
                try:
                    description.remove('\n')
                except:
                    pass
                description = ''.join(description)

                pathway_class = response.xpath("//nobr[contains(./text(),'Class')]/parent::*/parent::*/td//text()").extract()
                try:
                    pathway_class.remove('\n')
                except:
                    pass
                pathway_class = ''.join(pathway_class)

                bsid = ','.join(response.xpath("//a[contains(@href,'biosystems')]/text()").extract())
                goid = ','.join(response.xpath("//a[contains(@href,'GO:')]/text()").extract())

                pageurl = response.url
                if 'Global' in entry_value:
                    entry_value = entry_value.replace('Global','')

                # pathway_map_raw = ','.join(response.xpath("//nobr[contains(./text(),'map')]/parent::*/parent::*//a[text()='%s']/@href" %entry_value).extract())
                # pathway_map = 'http://www.kegg.jp'+pathway_map_raw
                # page_pathway = request.urlopen(pathway_map)
                # html_pathway = page_pathway.read()
                # html_pathway = html_pathway.decode('utf-8')
                # pathwaymap_url = 'http://www.kegg.jp' + ''.join(re.findall('<img src="(.*?)" name="pathwayimage"', html_pathway))
                if 'hsa' in entry_value:
                    pathwaymap_url ='http://www.kegg.jp/kegg/pathway/hsa/'+entry_value+'.png'
                if'map' in entry_value:
                    pathwaymap_url ='http://www.kegg.jp/kegg/pathway/map/'+entry_value+'.png'

                connection_store.execute("INSERT INTO {} (`pathway_code`,`pathway_name`,`description`,`class`,`BSID`,`GOID`,`page_url`,`pathwaymap_url`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)".format(output_table_keggpathway), entry_value, pathway_name, description, pathway_class, bsid, goid,pageurl,pathwaymap_url)

                Module_Code = response.xpath(
                    "//nobr[contains(./text(),'Module')]/parent::*/parent::*//a[contains(@href,'module')]/text()").extract()
                Module_raw = response.xpath("//nobr[contains(./text(),'Module')]/parent::*/parent::*//a[contains(@href,'show_pathway?')]/parent::*").extract()
                Module=[]
                if len(Module_raw)!=0:
                    for m in Module_raw:
                        Module.append(''.join(re.findall('>(.*?)<',m)))

                for i in range(0, len(Module_Code)):
                    connection_store.execute("INSERT INTO {} (`pathway_code`,`field_name`,`code`,`name`,`page_url`) VALUES(%s,'Module',%s,%s,%s)".format(output_table_pathway_otherinfo), entry_value, Module_Code[i], Module[i], pageurl)

                Disease =  response.xpath("//nobr[contains(./text(),'Disease')]/parent::*/parent::*//div/text()").extract()
                Disease_Code =  response.xpath("//nobr[contains(./text(),'Disease')]/parent::*/parent::*//a[contains(@href,'ds')]/text()").extract()
                for i in range(0,len(Disease_Code)):
                    connection_store.execute("INSERT INTO {} (`pathway_code`,`field_name`,`code`,`name`,`page_url`) VALUES(%s,'Disease',%s,%s,%s)".format(output_table_pathway_otherinfo),entry_value,Disease_Code[i],Disease[i],pageurl)

                Drug_Code = response.xpath("//nobr[contains(./text(),'Drug')]/parent::*/parent::*//a[contains(@href,'dr')]/text()").extract()
                Drug = response.xpath("//nobr[contains(./text(),'Drug')]/parent::*/parent::*//div/text()").extract()
                for i in range(0, len(Drug)):
                    connection_store.execute("INSERT INTO {} (`pathway_code`,`field_name`,`code`,`name`,`page_url`) VALUES(%s,'Drug',%s,%s,%s)".format(output_table_pathway_otherinfo), entry_value, Drug_Code[i], Drug[i], pageurl)

                Gene_code_lst = response.xpath("//nobr[contains(./text(),'Gene')]/parent::*/parent::*//a[contains(@href,'hsa')]/text()").extract()
                Gene_description = response.xpath("//nobr[contains(./text(),'Gene')]/parent::*/parent::*//a[contains(@href,'ko')]/parent::*").extract()
                Gene_description_lst = []
                for g in Gene_description:
                    Gene_description_lst.append(''.join(re.findall('>(.*?)<', g)))
                # print(Gene_description_lst)
                # if len(Gene_code_lst)==len(Gene_description_lst):
                for i in range(0,len(Gene_description_lst)):
                    connection_store.execute(
                        "INSERT INTO {} (`pathway_code`,`field_name`,`code`,`name`,`page_url`) VALUES(%s,'Gene',%s,%s,%s)".format(output_table_pathway_otherinfo), entry_value, Gene_code_lst[i], Gene_description_lst[i], pageurl)
                    print("insert ok!")

                # Compound_Code = response.xpath("//nobr[contains(./text(),'Compound')]/parent::*/parent::*//a/text()").extract()
                # Compound = response.xpath("//nobr[contains(./text(),'Compound')]/parent::*/parent::*//div/text()").extract()
                # if len(Compound) == len(Compound_Code):
                # for i in range(0, len(Compound)):
                #    connection_store.execute( "INSERT INTO {} (`pathway_code`,`field_name`,`code`,`name`,`page_url`) VALUES(%s,'Compound',%s,%s,%s)".format(output_table_pathway_otherinfo), entry_value, Compound_Code[i], Compound[i], pageurl)

        else:
            pass