# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
from bs4 import BeautifulSoup as bs
import unicodecsv
import os
import json
from ..items import SofangItem



class Spider(scrapy.Spider):
    name="sofang"
    allowed_domains = ['fang.com',"amap.com"]
    start_url="http://office.gz.fang.com/"

    def start_requests(self):
        for i in range(1,12):
            current_url=self.start_url+"zu/house-a075/i3"+str(i)+"/"
            yield Request(current_url,callback=self.parse,dont_filter=True)

    def parse(self, response):
        #信息提取
        page_content=response.text
        house_list=bs(page_content,"lxml").find_all("dd",class_="info rel floatr")
        for info in house_list:
            title=info.find('p', class_="gray6 mt15").find('a')["title"]
            address=info.find('p', class_="gray6 mt15").find('span',class_="iconAdress ml10 spAddr")["title"]
            area=info.find('div', class_="area area2 alignR").get_text()
            price=info.find('span', class_="price").get_text()
            m_price=info.find('p', class_="danjia alignR mt5 gray6").get_text()
            m_price=m_price.strip().split(u'元')[0]

            base_service = 'http://restapi.amap.com/v3/geocode/geo?address=' + u"广东省广州市"+address + '&output=JSON&key=d7c15ecb69b8274587837aada889b856'
            yield Request(base_service,callback=self.addressTolanlng,dont_filter=True,meta={'name': title,'address':address,'area':area,'price': float(price),'m_price':float(m_price)})

    #地理编码函数
    def addressTolanlng(self,response):
        item = SofangItem()
        result = json.loads(response.body)
        Xcoord, Ycoord = 0,0
        if result['info'] == "OK":
            try:
                latlng = result['geocodes'][0]["location"]
                longitude = latlng.split(",")[0]
                latitude = latlng.split(",")[1]
                Ycoord = float(latitude)
                Xcoord = float(longitude)
            except:
                print "sometning unknown wrong!"
        else:
            print u"地址编码失败"

        item['name']=response.meta['name']
        item['address'] = response.meta['address']
        item['area'] = response.meta['area']
        item['price'] = response.meta['price']
        item['m_price'] = response.meta['m_price']
        item['lon']=Xcoord
        item['lat'] = Ycoord
        return item