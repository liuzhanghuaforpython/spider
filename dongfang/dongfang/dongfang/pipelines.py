# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
class DongfangPipeline(object):
    #打开文件，保存为json数据
    def open_spider(self,spider):
        self.fp=open('dongfang.json','w',encoding="utf-8")
    #写入文件数据，转化为json字符串
    def process_item(self, item, spider):
        obj=dict(item)
        string=json.dumps(obj,ensure_ascii=False)
        self.fp.write(string)
        return item
    #关闭文件
    def close_spider(self,spider):
        self.fp.close()
