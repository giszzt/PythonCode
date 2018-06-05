# -*- coding: utf-8 -*-
import os
import unicodecsv
from items import SofangItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SofangPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,SofangItem):
            row_content=[item['name'],item['address'],item['area'],item['price'],item['m_price'],item['lon'],item['lat']]
            output_excel = "E:\\sofang.csv"
            field_names = [u"名字", u"地址", u"面积", u"平米价格", u"月租" ,"lon", "lat"]
            if os.path.isfile(output_excel) == False:
                with open(output_excel, 'w') as f:
                    w = unicodecsv.DictWriter(f, field_names,encoding='utf-8-sig')
                    w.writeheader()
                    # w.writerow(field_names)

            with open(output_excel, 'a') as f:
                w = unicodecsv.writer(f,encoding='utf-8-sig')
                w.writerow(row_content)
            return item