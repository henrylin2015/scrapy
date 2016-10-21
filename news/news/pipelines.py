# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class NewsPipeline(object):
    def process_item(self, item, spider):
        # print("desc:", item['desc'])
        # return item
        '''添加到数据库中'''
        sql = "INSERT INTO news(`title`, `desc`, `editor`, `source`, `public_time`, `link`)  VALUES('{}', '{}' ,'{}', '{}', '{}', '{}')".format(str(item['title']), str(item['desc']), str(item['editor']), str(item['source']), str(item['time']), str(item['link']))
        print("sql:", sql)
        mysql = connMysql()
        if mysql.insert(sql):
            print("insert OK")
        else:
            print("insert ON")

    def open_spider(self, spider):
        print("henry open spider")

    def close_spider(self, spider):
        print("henry close spider")


class connMysql(object):
    '''connect mysql'''
    conn = ""

    def __init__(self):
        try:
            self.conn = pymysql.connect(host='127.0.0.1', user='root',
                                        passwd=None, db="sina", charset="utf8")
        except Exception as e:
            print("henry error:", e)

    def insert(self, sql):
        flag = False
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            cur.close()
            flag = True
        except Exception as e:
            print("henry error1:", e)
            flag = False
        finally:
            self.sql_close()
        return flag

    def sql_close(self):
        if self.conn:
            self.conn.close()
