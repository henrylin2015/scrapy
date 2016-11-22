#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
import time

executable_path = 'plugin/phantomjs-2.1.1-macosx/bin/phantomjs'
driver = webdriver.PhantomJS(executable_path)
driver.get('http://image.baidu.com/search/index?tn=baiduimage&ps=1\
&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=高圆圆')
time.sleep(15)
pageSource = driver.page_source
print("info:", driver.find_element_by_id('imgid').text)
driver.close()
