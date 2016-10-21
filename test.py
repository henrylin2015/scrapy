#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
'''这个文件是测试正在表达式的'''
import re


s = str("<div class=\"article article_16\" id=\"artibody\"> \
        <p>\u3000\u3000原标题：辽宁铁岭市检察院副检察长赵宏伟接受组织调查30</p>\n' \
         '<p>\u3000\u3000中新网10月21日电据辽宁省纪委网站消息 \
，经中共铁岭市委批准，铁岭市人民检察院党组成员、副检察长赵宏伟（正处级）涉嫌严重违纪，目前正接受组织调查。</p>' \
         </div>")

print("str:", s)

reg = re.compile(r'<div.+?>([\s\S]*)</div>')
print("reg:", reg.findall(s))
